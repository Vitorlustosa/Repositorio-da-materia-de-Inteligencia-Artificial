import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Base de dados socioeconômicos de 18 países
# Variáveis: PIB per capita (USD) e Expectativa de vida (anos)
DADOS_PAISES = {
    'Pais': [
        'EUA', 'China', 'Japão', 'Alemanha', 'Brasil', 'Índia', 'Reino Unido',
        'França', 'Itália', 'Canadá', 'Coreia do Sul', 'Rússia', 'Austrália',
        'Espanha', 'México', 'Indonésia', 'Nigéria', 'África do Sul'
    ],
    'PIB_Per_Capita': [
        63543, 10500, 40246, 45723, 6796, 1900, 40284,
        38625, 31676, 43241, 31489, 10126, 51812,
        27057, 8346, 3869, 2097, 5090
    ],
    'Exp_Vida': [
        78.9, 76.9, 84.6, 81.3, 75.9, 69.7, 81.2,
        82.7, 83.5, 82.4, 83.0, 72.6, 82.9,
        83.5, 75.0, 71.7, 54.7, 64.1
    ]
}


def agrupar_paises():
    df = pd.DataFrame(DADOS_PAISES)
    features = df[['PIB_Per_Capita', 'Exp_Vida']]

    # A padronização (z-score) é indispensável aqui:
    # O PIB varia na casa de dezenas de milhares, enquanto a expectativa varia de 50 a 85.
    # Sem StandardScaler, a distância euclidiana do K-Means ignoraria a expectativa de vida.
    scaler = StandardScaler()
    features_escaladas = scaler.fit_transform(features)

    # Agrupamento em 3 clusters distintos (k=3)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(features_escaladas)

    print("=" * 65)
    print("  Clusterização de Países por Desenvolvimento (K-Means)")
    print("=" * 65)

    # Exibe resumo de cada grupo formado
    for c in sorted(df['Cluster'].unique()):
        grupo = df[df['Cluster'] == c]
        paises_str = ", ".join(grupo['Pais'])
        media_pib = grupo['PIB_Per_Capita'].mean()
        media_vida = grupo['Exp_Vida'].mean()

        print(f"\n--- Grupo {c} ({len(grupo)} países) ---")
        print(f"• Países               : {paises_str}")
        print(f"• Média PIB per Capita : ${media_pib:,.2f}")
        print(f"• Média Exp. de Vida   : {media_vida:.1f} anos")

    print("\n" + "=" * 65)

    # Visualização gráfica dos clusters
    plt.figure(figsize=(11, 6))
    cores = ['#2b5c8f', '#2a9d8f', '#e76f51']
    rotulos = ['Grupo 0', 'Grupo 1', 'Grupo 2']

    for c in range(3):
        grupo = df[df['Cluster'] == c]
        plt.scatter(
            grupo['PIB_Per_Capita'],
            grupo['Exp_Vida'],
            color=cores[c],
            label=rotulos[c],
            s=120,
            alpha=0.85,
            edgecolors='black',
            linewidths=1.2
        )

        for i in range(len(grupo)):
            nome = grupo['Pais'].iloc[i]
            x_pos = grupo['PIB_Per_Capita'].iloc[i]
            y_pos = grupo['Exp_Vida'].iloc[i]
            plt.annotate(
                nome,
                (x_pos, y_pos),
                xytext=(6, 4),
                textcoords='offset points',
                fontsize=8.5,
                weight='semibold'
            )

    plt.title('Clusterização de Países: Relação entre Renda e Expectativa de Vida (K-Means)', fontsize=12)
    plt.xlabel('PIB per Capita (USD)', fontsize=10)
    plt.ylabel('Expectativa de Vida (Anos)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title='Clusters Formados', frameon=True)
    plt.tight_layout()

    print("Exibindo gráfico dos clusters...")
    plt.show()


if __name__ == "__main__":
    agrupar_paises()