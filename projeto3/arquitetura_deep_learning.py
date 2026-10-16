import os
import time
import random
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms

# Configurações gerais de treinamento
DIRETORIO_DATASET = 'dataset'
NUM_EPOCAS = 5
BATCH_SIZE = 32
LEARNING_RATE = 0.001


def obter_dispositivo():
    """Detecta se há GPU aceleradora disponível (CUDA) ou utiliza a CPU."""
    disp = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"• Dispositivo de processamento selecionado: {disp}")
    return disp


def preparar_transformacoes():
    """
    Define os pipelines de pré-processamento e data augmentation:
    - Treinamento: RandomResizedCrop e RandomHorizontalFlip para generalização
    - Validação/Teste: Redimensionamento e corte central determinístico
    - Normalização padrão ImageNet (médias e desvios por canal RGB)
    """
    media_imagenet = [0.485, 0.456, 0.406]
    std_imagenet = [0.229, 0.224, 0.225]

    return {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(media_imagenet, std_imagenet)
        ]),
        'validation': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(media_imagenet, std_imagenet)
        ])
    }


def carregar_dados(data_dir, batch_size=BATCH_SIZE):
    """Carrega as imagens organizadas em subpastas por classe usando ImageFolder."""
    if not os.path.exists(data_dir):
        print(f"\n[Aviso] Diretório '{data_dir}' não encontrado.")
        print("Para treinar a rede, organize o dataset na seguinte estrutura:")
        print("  dataset/")
        print("    ├── train/")
        print("    │    ├── classe_A/")
        print("    │    └── classe_B/")
        print("    └── validation/")
        print("         ├── classe_A/")
        print("         └── classe_B/\n")
        return None, None, None, None

    transforms_map = preparar_transformacoes()

    datasets_img = {
        fase: datasets.ImageFolder(os.path.join(data_dir, fase), transforms_map[fase])
        for fase in ['train', 'validation']
    }

    dataloaders = {
        fase: torch.utils.data.DataLoader(datasets_img[fase], batch_size=batch_size, shuffle=(fase == 'train'))
        for fase in ['train', 'validation']
    }

    tamanhos = {fase: len(datasets_img[fase]) for fase in ['train', 'validation']}
    classes = datasets_img['train'].classes

    return dataloaders, tamanhos, classes, transforms_map['validation']


def construir_modelo(num_classes):
    """
    Aplica Transfer Learning com MobileNetV2:
    1. Importa pesos pré-treinados na ImageNet (extração de features rica)
    2. Congela os parâmetros convolucionais para preservar filtros aprendidos
    3. Substitui a camada linear final pela dimensão do nosso conjunto de classes
    """
    modelo = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

    # Congela convoluções
    for parametro in modelo.parameters():
        parametro.requires_grad = False

    # Substitui a última camada densa do classificador
    in_features = modelo.classifier[1].in_features
    modelo.classifier[1] = nn.Linear(in_features, num_classes)

    return modelo


def testar_amostra(modelo, classes, transformacao, dispositivo):
    """Sorteia uma imagem do conjunto de validação e realiza a inferência visual."""
    val_dir = os.path.join(DIRETORIO_DATASET, 'validation')
    if not os.path.exists(val_dir):
        return

    raças = os.listdir(val_dir)
    if not raças:
        return

    raça_sorteada = random.choice(raças)
    pasta_raça = os.path.join(val_dir, raça_sorteada)
    arquivos = [f for f in os.listdir(pasta_raça) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not arquivos:
        return

    caminho_imagem = os.path.join(pasta_raça, random.choice(arquivos))

    modelo.eval()
    imagem_pil = Image.open(caminho_imagem).convert('RGB')
    tensor_img = transformacao(imagem_pil).unsqueeze(0).to(dispositivo)

    with torch.no_grad():
        saida = modelo(tensor_img)
        probabilidades = torch.nn.functional.softmax(saida[0], dim=0)
        confianca, idx_previsto = torch.max(probabilidades, 0)

    classe_predita = classes[idx_previsto]
    percentual = confianca.item() * 100

    print("\n" + "=" * 45)
    print("        INFERÊNCIA EM IMAGEM DE TESTE")
    print("=" * 45)
    print(f"• Imagem Avaliada : {caminho_imagem}")
    print(f"• Classe Real     : {raça_sorteada.upper()}")
    print(f"• Previsão da Rede: {classe_predita.upper()}")
    print(f"• Confiança       : {percentual:.2f}%")
    status = "ACERTOU!" if classe_predita == raça_sorteada else "ERROU (necessita mais épocas)."
    print(f"• Resultado       : {status}")
    print("=" * 45)


def treinar_modelo():
    print("=" * 60)
    print("  Transfer Learning com MobileNetV2 (PyTorch)")
    print("=" * 60)

    dispositivo = obter_dispositivo()
    dataloaders, tamanhos, classes, transform_val = carregar_dados(DIRETORIO_DATASET)

    if dataloaders is None:
        return

    print(f"• Classes encontradas ({len(classes)}): {', '.join(classes)}")
    print(f"• Amostras de treino: {tamanhos['train']} | Validação: {tamanhos['validation']}\n")

    modelo = construir_modelo(len(classes)).to(dispositivo)
    criterio = nn.CrossEntropyLoss()
    otimizador = optim.Adam(modelo.classifier[1].parameters(), lr=LEARNING_RATE)

    t_inicio = time.time()

    for epoca in range(NUM_EPOCAS):
        print(f"Época {epoca + 1}/{NUM_EPOCAS}")
        print("-" * 25)

        for fase in ['train', 'validation']:
            if fase == 'train':
                modelo.train()
            else:
                modelo.eval()

            perda_acumulada = 0.0
            acertos_acumulados = 0

            for entradas, rotulos in dataloaders[fase]:
                entradas = entradas.to(dispositivo)
                rotulos = rotulos.to(dispositivo)

                otimizador.zero_grad()

                with torch.set_grad_enabled(fase == 'train'):
                    saidas = modelo(entradas)
                    _, predicoes = torch.max(saidas, 1)
                    perda = criterio(saidas, rotulos)

                    if fase == 'train':
                        perda.backward()
                        otimizador.step()

                perda_acumulada += perda.item() * entradas.size(0)
                acertos_acumulados += torch.sum(predicoes == rotulos.data)

            perda_fase = perda_acumulada / tamanhos[fase]
            acuracia_fase = acertos_acumulados.double() / tamanhos[fase]

            print(f"[{fase.upper():<10}] Loss: {perda_fase:.4f} | Acurácia: {acuracia_fase*100:.2f}%")
        print()

    tempo_total = time.time() - t_inicio
    print(f"Treinamento finalizado em {tempo_total // 60:.0f}m {tempo_total % 60:.0f}s")

    # Salva os pesos treinados
    arquivo_pesos = "modelo_mobilenet_custom.pth"
    torch.save(modelo.state_dict(), arquivo_pesos)
    print(f"Pesos do modelo exportados para: {arquivo_pesos}")

    # Teste de amostra individual
    testar_amostra(modelo, classes, transform_val, dispositivo)


if __name__ == "__main__":
    treinar_modelo()