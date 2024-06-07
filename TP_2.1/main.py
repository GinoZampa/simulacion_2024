from gcl import GCL
from mid_square import MediosCuadrados
import numpy as np
from scipy.stats import kstest
import time
from scipy.stats import chi2
import matplotlib.pyplot as plt
import json
import os
import argparse

parser = argparse.ArgumentParser(description="Simulador de ruleta")
parser.add_argument("-c", default=30000, type=int, help="Número de pruebas")
parser.add_argument("-s", default=1000, type=int, help="seed")
args = parser.parse_args()
largo_secuencia = args.c
seed = args.s

if largo_secuencia < 1:
    print("El número de pruebas debe ser mayor a 0")
    exit()
if largo_secuencia <= 5000:
    size_puntos_graficos = 15
if largo_secuencia > 5000 and args.s <= 20000:
    size_puntos_graficos = 10
if largo_secuencia > 20000:
    size_puntos_graficos = 3
seed = int(time.time()) # Usar el tiempo actual como semilla, las misma para los 2 test

################################RUTAS################################
# Obtener la ruta completa del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))
# Crear directorio para guardar los datos
# ruta_datos = os.path.join(directorio_actual, 'datos_json')
# if not os.path.exists(ruta_datos):
#     os.makedirs(ruta_datos)
#crea al directorio para guardar las graficas
ruta_graficas = os.path.join(directorio_actual, 'graficas/')
if not os.path.exists(ruta_graficas):
    os.makedirs(ruta_graficas)

def genCL(seed, n, a=1103515245, c=12345, m=2**31):
    gcl = GCL(seed, a, c, m)
    return gcl.generar_secuencia(n)

def genCuad(seed, n):
    digitos=4
    ms_generator = MediosCuadrados(seed, digitos)
    return ms_generator.generar_secuencia(n) 

def test_media(secuencia):
    print("Test media")
    n = len(secuencia)
    media = np.mean(secuencia)
    media_esp = 0.5
    media_test = abs(media - media_esp) < (1 / np.sqrt(12 * n))
    print("    Media: ", media)
    print("    Media esperada: ", media_esp)
    print("    Paso el test de media: ", media_test)

def test_chi_cuadrado(secuencia, k=10):
    print("Test Chi-cuadrado")
    n = len(secuencia)
    frecuencia_esp = n / k
    frecuencia_obs, _ = np.histogram(secuencia, bins=k, range=(0.0, 1.0))
    chi_cuadrado = np.sum((frecuencia_obs - frecuencia_esp)**2 / frecuencia_obs)
    valor_critico = chi2.ppf(0.95, df=k-1)
    pasa_test = chi_cuadrado < valor_critico
    print("    Estadistico: ", chi_cuadrado)
    print("    Valor critico: ", valor_critico)
    print("    Paso es test de Chi-cuadrado: ", pasa_test)

def test_autocorrelacion(secuencia, lag=1):
    print("Test Chi-cuadrado")
    n = len(secuencia)
    media = np.mean(secuencia)
    varianza = np.var(secuencia)
    if varianza == 0:
        print("    Varianza =  0, no se puede desarrollar el test de autocorrelación")
        return False
    autocovarianza = np.mean([(secuencia[i] - media) * (secuencia[i + lag] - media) for i in range(n - lag)])
    autocorrelacion = autocovarianza / varianza
    intervalo_confianza = 1.96 / np.sqrt(n)
    pasa_test = abs(autocorrelacion) < intervalo_confianza
    print("    Autocorrelacion (lag ", lag,"): ", autocorrelacion)
    print("    95% Intervalo de confianza: ", intervalo_confianza)
    print("    Paso el test de la Autocorrelacion: ", pasa_test)

def test_kolmogorov_smirnov(secuencia):
    print("Test Kolmogorov-Smirnov")
    estadistico, valor_p = kstest(secuencia, 'uniform')
    print("    Estadistico Kolmogorov-Smirnov: ", estadistico)
    print("    Valor_p: ", valor_p)
    alpha = 0.05  # Nivel de significancia del 5%
    pasa_test = valor_p > alpha
    print("    Paso el test de Kolmogorov-Smirnov: ", pasa_test)

def grafica_dispersion(p, nombre=""):
    plt.figure(figsize=(14, 8))
    plt.scatter(range(len(p)), p, label=nombre, color='black', s=size_puntos_graficos)
    plt.xlabel('Índice')
    plt.ylabel('Número Pseudoaleatorio')
    plt.title(f'Gráfico de Dispersión de Números Pseudoaleatorios: {nombre}. N={largo_secuencia}')

    dispersion = os.path.join(ruta_graficas, f'dispersion_{nombre}_{largo_secuencia}.png')
    plt.savefig(dispersion)
    plt.close()  

def grafica_dispersion_comparacion(p1, p2, p3):
    plt.figure(figsize=(14, 8))
    plt.scatter(range(len(p1)), p1, label='GCL', color='blue', alpha=0.5, s=size_puntos_graficos)
    plt.scatter(range(len(p2)), p2, label='Medios Cuadrados', color='red', alpha=0.2, s=size_puntos_graficos)
    plt.scatter(range(len(p3)), p3, label='Numpy', color='green', alpha=0.5, s=size_puntos_graficos)
    plt.xlabel('Índice')
    plt.ylabel('Número Pseudoaleatorio')
    plt.title(f'Gráfico de Dispersión de Números Pseudoaleatorios: Comparación. N={largo_secuencia}')
    plt.legend()  

    dispersion = os.path.join(ruta_graficas, f'dispersion_comparacion_{largo_secuencia}.png')
    plt.savefig(dispersion)
    plt.close()  

def gafica_histograma(secuencia, k=10, nombre=""):
    n = len(secuencia)
    frecuencia_esp = n / k
    plt.figure(figsize=(10, 6))
    plt.hist(secuencia, label="Frecuencia Observada" , bins=k, range=(0.0, 1.0), color='green', alpha=0.4, edgecolor='b')
    plt.plot([0, 1], [frecuencia_esp, frecuencia_esp], 'r--', label="Frecuencia Esperada", lw=2)
    plt.xlabel('Intervalos')
    plt.ylabel('Frecuencia')
    plt.title(f'Histograma de Frecuencias: {nombre}. N={largo_secuencia}')
    plt.legend()

    histograma = os.path.join(ruta_graficas, f'frecuencias_{nombre}_{largo_secuencia}.png')
    plt.savefig(histograma)
    plt.close()

if __name__ == "__main__":    
    sec1 = genCL(seed,largo_secuencia)
    gafica_histograma(sec1, 10, "GCL")
    grafica_dispersion(sec1, "GCL")
    test_media(sec1)
    test_chi_cuadrado(sec1)
    test_autocorrelacion(sec1)
    test_kolmogorov_smirnov(sec1)

    sec2 = genCuad(seed,largo_secuencia)
    gafica_histograma(sec2, 10, "Medios_Cuadrados")
    grafica_dispersion(sec2, "Medios_Cuadrados")
    test_media(sec2)
    test_chi_cuadrado(sec2)
    test_autocorrelacion(sec2)
    test_kolmogorov_smirnov(sec2)

    sec3 = np.random.rand(largo_secuencia)
    gafica_histograma(sec3, 10, "Numpy")
    grafica_dispersion(sec3, "Numpy")
    grafica_dispersion_comparacion(sec1, sec2, sec3)
