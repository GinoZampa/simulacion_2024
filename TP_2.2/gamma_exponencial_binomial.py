import numpy as np
import matplotlib.pyplot as plt
import math
import os
import argparse
import time

parser = argparse.ArgumentParser(description="Simulador de ruleta")
parser.add_argument("-n", default=10000, type=int, help="Número de pruebas")
parser.add_argument("-s", default=1000, type=int, help="seed")
args = parser.parse_args()
largo_secuencia = args.n
seed = args.s

if largo_secuencia < 1:
    print("El número de pruebas debe ser mayor a 0")
    exit()
if largo_secuencia <= 5000:
    size_puntos_graficos = 15
if largo_secuencia > 5000 and largo_secuencia <= 20000:
    size_puntos_graficos = 10
if largo_secuencia > 20000:
    size_puntos_graficos = 3
seed = int(time.time()) # Usar el tiempo actual como semilla, las misma para los 2 test

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

def dist_binomial(n, p, size):
    """
    Genera números aleatorios de una distribución binomial usando el método de rechazo.

    :param n: Número de ensayos.
    :param p: Probabilidad de éxito en cada ensayo.
    :param size: Número de muestras a generar.
    :return: Un arreglo de números aleatorios con distribución binomial.
    """
    def binomial_pmf(k, n, p):
      """
      Calcula la PMF de una distribución binomial.
      """
      comb = math.comb(n, k)
      return comb * (p ** k) * ((1 - p) ** (n - k))
  
    samples = []
    max_pmf = binomial_pmf(n // 2, n, p)  # Usar el valor máximo de la PMF para el método de rechazo
    for _ in range(size):
      while True:
        # Generar un candidato k de una distribución uniforme discreta [0, n]
        k = np.random.randint(0, n + 1)
        # Generar una muestra uniforme u para la decisión de aceptación
        u = np.random.uniform(0, max_pmf)
        # Evaluar la PMF binomial en k
        pmf_k = binomial_pmf(k, n, p)
        # Condición de aceptación
        if u < pmf_k:
            samples.append(k)
            break
    return np.array(samples)
  
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
    if "Numpy" in nombre:
      histograma = os.path.join(ruta_graficas_numpy, f'histograma_{nombre}.png')
      color = 'limegreen'
    elif "comparacion" in nombre: color = ['limegreen', 'royalblue']
    else:
      color = 'royalblue'
      histograma = os.path.join(ruta_graficas, f'histograma_{nombre}.png')
    if "Binomial" in nombre: bins = np.arange(0, 21) - 0.5
    else: bins = 40
    plt.hist(datos, bins=bins, edgecolor='black', color=color)
    plt.title(f'Histograma de Frecuencias: {nombre}. N={largo_secuencia}')
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    if "Numpy" in nombre:
      histograma = os.path.join(ruta_graficas_numpy, f'histograma_{nombre}.png')
    else:
      histograma = os.path.join(ruta_graficas, f'histograma_{nombre}.png')
    plt.savefig(histograma)
    plt.close()

def graficar_dispersion(datos, nombre=""):
    if "Numpy" in nombre:
      dispersion = os.path.join(ruta_graficas_numpy, f'dispersion_{nombre}.png')
      color = 'limegreen'
    else:
      dispersion = os.path.join(ruta_graficas, f'dispersion_{nombre}.png')
      color = 'royalblue'
    plt.figure(figsize=(14, 8))
    plt.scatter(range(len(datos)), datos, label=nombre, color=color, s=size_puntos_graficos)
    plt.xlabel('Índice')
    plt.ylabel('Número Pseudoaleatorio')
    plt.title(f'Gráfico de Dispersión de Números Pseudoaleatorios: {nombre}. N={largo_secuencia}')
    plt.savefig(dispersion)
    plt.close()

def exponencial():
  sec_e = np.random.exponential(3, largo_secuencia)
  datos_exponencial = dist_exponencial(1/3, largo_secuencia)
  # Graficamos la distribución exponencial
  graficar_histograma(datos_exponencial, "Exponencial")
  graficar_dispersion(datos_exponencial, "Exponencial")
  graficar_histograma(sec_e, "Numpy-Exponencial")
  graficar_dispersion(sec_e, "Numpy-Exponencial")
  graficar_histograma([sec_e, datos_exponencial], "Exponencial-comparacion")

def gamma():
  sec_g = np.random.gamma(5, 1, largo_secuencia)
  datos_gamma = dist_gamma(5,1, largo_secuencia)
  # Graficamos la distribución gamma
  graficar_histograma(datos_gamma, "Gamma")
  graficar_dispersion(datos_gamma, "Gamma")
  graficar_histograma(sec_g, "Numpy-Gamma")
  graficar_dispersion(sec_g, "Numpy-Gamma")
  graficar_histograma([sec_g, datos_gamma], "Gamma-comparacion")


def binomial():
  #ensayos(x) = 10, probabilidad(p) = 0.5, tamaño = 10000
  sec_b = np.random.binomial(20, 0.1, largo_secuencia)
  datos_binomial = dist_binomial(20, 0.1, largo_secuencia)
  graficar_histograma(datos_binomial, "Binomial")
  graficar_dispersion(datos_binomial, "Binomial")  
  # Graficamos la distribución binomial
  graficar_histograma(sec_b, "Numpy-Binomial")
  graficar_dispersion(sec_b, "Numpy-Binomial")
  graficar_histograma([sec_b, datos_binomial], "Binomial-comparacion")


if __name__ == "__main__":
  binomial()
  exponencial()
  gamma()