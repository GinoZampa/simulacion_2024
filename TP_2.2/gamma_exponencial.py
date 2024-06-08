import numpy as np
import matplotlib.pyplot as plt
import math
import os

################################RUTAS################################
# Obtener la ruta completa del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_graficas = os.path.join(directorio_actual, 'graficas/')
if not os.path.exists(ruta_graficas):
    os.makedirs(ruta_graficas)
ruta_graficas_numpy = os.path.join(ruta_graficas, 'numpy/')
if not os.path.exists(ruta_graficas_numpy):
    os.makedirs(ruta_graficas_numpy)

# Definimos la distribución exponencial
def dist_exponencial(lambd, largo_secuencia_exponencial):
    # Generamos la secuencia de números pseudoaleatorios
    secuencia = np.random.uniform(0, 1, largo_secuencia_exponencial)
    # Generación de la distribución exponencial con metodo de inversion
    datos_exponencial = [-math.log(x) / lambd for x in secuencia]
    return datos_exponencial

# def dist_gamma(beta, largo_secuencia_gamma):
#     # Generamos la secuencia de números pseudoaleatorios
#     secuencia = np.random.uniform(0, 1, largo_secuencia_gamma)
#     # Generación de la distribución gamma con metodo de inversion
#     datos_gamma = [-beta * math.log(x) for x in secuencia]
#     return datos_gamma

#generador de numeros con distribucion gamma
def dist_gamma(shape_param, scale_param, size):
    """
    Genera números aleatorios de una distribución Gamma usando el método de aceptación-rechazo.

    :param shape_param: Parámetro de forma (k) de la distribución Gamma.
    :param scale_param: Parámetro de escala (θ) de la distribución Gamma.
    :param size: Número de muestras a generar.
    :return: Un arreglo de números aleatorios con distribución Gamma.
    """
    if shape_param < 1:
        shape_param += 1
        u = np.random.uniform(0, 1, size)
        gamma_sample = dist_gamma(shape_param, scale_param, size)
        return gamma_sample * np.power(u, 1.0 / shape_param)

    d = shape_param - 1/3
    c = 1 / np.sqrt(9 * d)

    samples = []
    for _ in range(size):
        while True:
            x = np.random.normal(0, 1)
            v = (1 + c * x) ** 3
            u = np.random.uniform(0, 1)
            if u < 1 - 0.0331 * (x ** 4):
                break
            if np.log(u) < 0.5 * x ** 2 + d * (1 - v + np.log(v)):
                break
        samples.append(d * v)

    return np.array(samples) * scale_param

def graficar_histograma(datos, nombre=""):
    plt.figure(figsize=(14, 8))
    # Graficamos la distribución exponencial
    plt.hist(datos, bins=20, edgecolor='black', alpha=0.7)
    plt.title("Distribución Exponencial")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    if "Numpy" in nombre:
      histograma = os.path.join(ruta_graficas_numpy, f'histograma_{nombre}.png')
    else:
      histograma = os.path.join(ruta_graficas, f'histograma_{nombre}.png')
    plt.savefig(histograma)
    plt.close()

def graficar_dispersion(datos, nombre=""):
    plt.figure(figsize=(14, 8))
    plt.scatter(range(len(datos)), datos, label=nombre, color='black', s=10)
    plt.xlabel('Índice')
    plt.ylabel('Número Pseudoaleatorio')
    plt.title(f'Gráfico de Dispersión de Números Pseudoaleatorios: {nombre}. N={len(datos)}')
    if "Numpy" in nombre:
      dispersion = os.path.join(ruta_graficas_numpy, f'dispersion_{nombre}.png')
    else:
      dispersion = os.path.join(ruta_graficas, f'dispersion_{nombre}.png')
    plt.savefig(dispersion)
    plt.close()

def exponencial():
  sec_e = np.random.exponential(2, 10000)
  datos_exponencial = dist_exponencial(2, 10000)
  # Graficamos la distribución exponencial
  graficar_histograma(datos_exponencial, "Exponencial")
  graficar_dispersion(datos_exponencial, "Exponencial")
  graficar_histograma(sec_e, "Numpy-Exponencial")
  graficar_dispersion(sec_e, "Numpy-Exponencial")

def gamma():
  sec_g = np.random.gamma(5, 1, 10000)
  datos_gamma = dist_gamma(5,1, 10000)
  # Graficamos la distribución gamma
  graficar_histograma(datos_gamma, "Gamma")
  graficar_dispersion(datos_gamma, "Gamma")
  graficar_histograma(sec_g, "Numpy-Gamma")
  graficar_dispersion(sec_g, "Numpy-Gamma")

if __name__ == "__main__":
  exponencial()
  gamma()