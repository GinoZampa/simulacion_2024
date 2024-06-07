from gcl import GCL
from mid_square import MediosCuadrados
import numpy as np
from scipy.stats import kstest
import time
from scipy.stats import chi2
import matplotlib.pyplot as plt

def genCL(n, a=1103515245, c=12345, m=2**31):
    seed = int(time.time())  # Usar el tiempo actual como semilla
    gcl = GCL(seed, a, c, m)
    return gcl.generar_secuencia(n)

def genCuad(n):
    seed = int(time.time())  # Usar el tiempo actual como semilla
    digitos=4
    ms_generator = MediosCuadrados(seed, digitos)
    return ms_generator.generar_secuencia(n) 

def test_media(secuencia):
    n = len(secuencia)
    media = np.mean(secuencia)
    media_esp = 0.5
    media_test = abs(media - media_esp) < (1 / np.sqrt(12 * n))
    print("Media: ", media)
    print("Media esperada: ", media_esp)
    print("Paso el test de media: ", media_test)

def test_chi_cuadrado(secuencia, k=10):
    n = len(secuencia)
    frecuencia_esp = n / k
    frecuencia_obs, _ = np.histogram(secuencia, bins=k, range=(0.0, 1.0))
    chi_cuadrado = np.sum((frecuencia_obs - frecuencia_esp)**2 / frecuencia_obs)
    valor_critico = chi2.ppf(0.95, df=k-1)
    pasa_test = chi_cuadrado < valor_critico
    print("Estadistico: ", chi_cuadrado)
    print("Valor critico: ", valor_critico)
    print("Paso es test de Chi-cuadrado: ", pasa_test)

def test_autocorrelacion(secuencia, lag=1):
    n = len(secuencia)
    media = np.mean(secuencia)
    varianza = np.var(secuencia)
    if varianza == 0:
        print("Varianza =  0, no se puede desarrollar el test de autocorrelación")
        return False
    autocovarianza = np.mean([(secuencia[i] - media) * (secuencia[i + lag] - media) for i in range(n - lag)])
    autocorrelacion = autocovarianza / varianza
    intervalo_confianza = 1.96 / np.sqrt(n)
    pasa_test = abs(autocorrelacion) < intervalo_confianza
    print("Autocorrelacion (lag ", lag,"): ", autocorrelacion)
    print("95% Intervalo de confianza: ", intervalo_confianza)
    print("Paso el test de la Autocorrelacion: ", pasa_test)


def test_kolmogorov_smirnov(secuencia):
    estadistico, valor_p = kstest(secuencia, 'uniforme')
    print("Estadistico Kolmogorov-Smirnov: ", estadistico)
    print("Valor_p: ", valor_p)
    alpha = 0.05  # Nivel de significancia del 5%
    pasa_test = valor_p > alpha
    print("Paso el test de Kolmogorov-Smirnov: ", pasa_test)

def grafica(p1, p2, p3):
    fig, axs = plt.subplots()
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(sec1)), sec1, label='GCL', color='blue', alpha=0.5)
    plt.scatter(range(len(sec2)), sec2, label='Medios Cuadrados', color='red', alpha=0.5)
    plt.scatter(range(len(sec3)), sec3, label='Numpy', color='green', alpha=0.5)
    plt.xlabel('Índice')
    plt.ylabel('Número Pseudoaleatorio')
    plt.title('Gráfico de Dispersión de Números Pseudoaleatorios')
    plt.legend()
    plt.show()

if __name__ == "__main__":
  sec1 = genCL(1000)
  test_media(sec1)
  test_chi_cuadrado(sec1)
  test_autocorrelacion(sec1)
  test_kolmogorov_smirnov(sec1)
  sec2 = genCuad(1000)
  test_media(sec2)
  test_chi_cuadrado(sec2)
  test_autocorrelacion(sec2)
  test_kolmogorov_smirnov(sec2)
  sec3 = np.random.rand(1000)
  grafica(sec1, sec2, sec3)
