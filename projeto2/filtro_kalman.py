import numpy as np
import matplotlib.pyplot as plt

def gerar_trajetoria_helicoptero(n_pontos=120, seed=42):
    """
    Simula o voo tridimensional suave de um helicóptero:
    - Movimento helicoidal/ondulatório nos eixos X, Y e Z
    - Adiciona ruído gaussiano para simular leituras imprecisas de sensores (GPS/altímetro).
    """
    np.random.seed(seed)
    t = np.linspace(0, 12, n_pontos)

    # Trajetória suave real
    real_x = 50.0 + 15.0 * np.sin(t * 0.8)
    real_y = 40.0 + 12.0 * np.cos(t * 0.8)
    real_z = 20.0 + 8.0 * np.sin(t * 0.4) + 1.5 * t

    trajetoria_real = np.vstack([real_x, real_y, real_z]).T

    # Medições com ruído sensorial (variância = 4.0, desvio padrão = 2.0)
    ruido = np.random.normal(loc=0.0, scale=2.0, size=trajetoria_real.shape)
    medicoes_ruidosas = trajetoria_real + ruido

    return trajetoria_real, medicoes_ruidosas


def filtro_kalman_3d(medicoes, variancia_processo=0.8, variancia_medicao=4.0):
    """
    Filtro de Kalman 1D desacoplado para cada um dos eixos espaciais (X, Y, Z).
    Equações fundamentais em cada passo:
      1. Predição da incerteza:  P = P + Q
      2. Ganho de Kalman:        K = P / (P + R)
      3. Atualização de estado:  x = x + K * (z - x)
      4. Atualização da certeza: P = (1 - K) * P
    """
    n_pontos, dims = medicoes.shape
    estimativas = np.zeros_like(medicoes)

    # Chute inicial do estado e incerteza inicial
    estado = np.array([50.0, 40.0, 20.0], dtype=float)
    incerteza = np.array([2.0, 2.0, 2.0], dtype=float)

    for i in range(n_pontos):
        z = medicoes[i]

        # Etapa 1: Predição
        incerteza = incerteza + variancia_processo

        # Etapa 2: Ganho de Kalman
        K = incerteza / (incerteza + variancia_medicao)

        # Etapa 3: Correção da estimativa com a medição
        estado = estado + K * (z - estado)

        # Etapa 4: Atualização da incerteza
        incerteza = (1.0 - K) * incerteza

        estimativas[i] = estado

    return estimativas


def calcular_rmse(real, estimado):
    return np.sqrt(np.mean((real - estimado) ** 2))


if __name__ == "__main__":
    print("=== Rastreamento de Trajetória 3D com Filtro de Kalman ===")

    real, medicoes = gerar_trajetoria_helicoptero(n_pontos=120)
    estimado = filtro_kalman_3d(medicoes, variancia_processo=0.8, variancia_medicao=4.0)

    # Avaliação de desempenho da filtragem
    rmse_sensor = calcular_rmse(real, medicoes)
    rmse_kalman = calcular_rmse(real, estimado)
    reducao_erro = (1.0 - rmse_kalman / rmse_sensor) * 100

    print(f"• Erro médio do sensor (ruidoso) : {rmse_sensor:.3f} m")
    print(f"• Erro após o Filtro de Kalman   : {rmse_kalman:.3f} m")
    print(f"• Redução do erro               : {reducao_erro:.1f}%\n")

    # Plot comparativo 3D
    fig = plt.figure(figsize=(15, 6))

    # Gráfico 1: Trajetória Real vs Medições Ruidosas
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(real[:, 0], real[:, 1], real[:, 2], label="Trajetória Real", color="green", linewidth=2.5)
    ax1.scatter(medicoes[:, 0], medicoes[:, 1], medicoes[:, 2], label="Medições Ruidosas", color="red", alpha=0.35, s=15)
    ax1.set_title("Medições de Sensores (com Ruído)")
    ax1.set_xlabel("X (m)")
    ax1.set_ylabel("Y (m)")
    ax1.set_zlabel("Z (m)")
    ax1.legend()

    # Gráfico 2: Trajetória Real vs Estimativa Filtrada
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot(real[:, 0], real[:, 1], real[:, 2], label="Trajetória Real", color="green", linewidth=2.5)
    ax2.plot(estimado[:, 0], estimado[:, 1], estimado[:, 2], label="Filtro de Kalman", color="blue", linewidth=2.0, linestyle="--")
    ax2.set_title(f"Trajetória Filtrada (RMSE: {rmse_kalman:.2f}m vs Sensor: {rmse_sensor:.2f}m)")
    ax2.set_xlabel("X (m)")
    ax2.set_ylabel("Y (m)")
    ax2.set_zlabel("Z (m)")
    ax2.legend()

    plt.tight_layout()
    print("Feche a janela do gráfico para finalizar a execução.")
    plt.show()
