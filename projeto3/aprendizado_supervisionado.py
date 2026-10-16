import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

sns.set_theme(style="whitegrid")

def gerar_dados_consumo(n_amostras=100, seed=42):
    """
    Simula o impacto da temperatura ambiente no consumo elétrico residencial:
    Dias mais quentes exigem maior uso de ar-condicionado e refrigeração.
    """
    np.random.seed(seed)
    # Temperatura média diária variando entre 20°C e 35°C
    temperaturas = np.linspace(20, 35, n_amostras) + np.random.normal(0, 0.8, n_amostras)
    X = temperaturas.reshape(-1, 1)

    # Relação linear com ruído estocástico: Consumo = 100 + 15 * Temp + erro
    ruido = np.random.normal(0, 45, size=X.shape)
    y = (100.0 + 15.0 * X + ruido).flatten()

    df = pd.DataFrame({
        'Temperatura_C': X.flatten(),
        'Consumo_kWh': y
    })
    return X, y, df


def treinar_e_avaliar():
    X, y, df = gerar_dados_consumo()

    # Divisão 80% treino e 20% teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    # Avaliação de métricas
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("=" * 55)
    print("  Regressão Linear: Temperatura vs Consumo de Energia")
    print("=" * 55)
    print(f"• Equação da Reta : Consumo = {modelo.intercept_:.2f} + {modelo.coef_[0]:.2f} * Temp")
    print(f"• Inclinação (a)  : {modelo.coef_[0]:.2f} kWh por cada 1°C adicional")
    print(f"• Intercepto (b)  : {modelo.intercept_:.2f} kWh (consumo base)")
    print("-" * 55)
    print(f"• Erro Médio (RMSE)        : {rmse:.2f} kWh")
    print(f"• Coef. Determinação (R²) : {r2:.4f} (explica {r2*100:.1f}% da variância)")
    print("=" * 55)

    # Visualização com Matplotlib / Seaborn
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico 1: Dispersão dos dados simulados
    sns.scatterplot(x='Temperatura_C', y='Consumo_kWh', data=df, ax=axs[0], color='royalblue', alpha=0.7)
    axs[0].set_title("Análise Exploratória: Dispersão Bruta")
    axs[0].set_xlabel("Temperatura Média Diária (°C)")
    axs[0].set_ylabel("Consumo Residencial (kWh)")

    # Gráfico 2: Ajuste do modelo no conjunto de teste
    axs[1].scatter(X_test, y_test, color='darkblue', alpha=0.7, label='Dados Reais (Teste)')
    # Ordena para linha contínua perfeita
    idx_ordenado = np.argsort(X_test.flatten())
    axs[1].plot(X_test[idx_ordenado], y_pred[idx_ordenado], color='crimson', linewidth=2.5, label=f'Reta Ajustada (R²={r2:.2f})')
    axs[1].set_title("Avaliação do Modelo: Reta de Regressão Linear")
    axs[1].set_xlabel("Temperatura Média Diária (°C)")
    axs[1].set_ylabel("Consumo Residencial (kWh)")
    axs[1].legend()

    plt.tight_layout()
    print("\nExibindo gráficos comparativos...")
    plt.show()


if __name__ == "__main__":
    treinar_e_avaliar()
