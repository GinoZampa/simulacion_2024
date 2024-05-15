import json
import random
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

#################################ARGUMENTOS DE ENTRADA################################

parser = argparse.ArgumentParser(description="Simulador de ruleta")
parser.add_argument("-c", default=2000, type=int, help="Número de tiradas")
parser.add_argument("-n", default=1, type=int, help="Número de corridas")
parser.add_argument("-e", default="r", choices=["r","n"], help="Color a apostar")
parser.add_argument("-s", default="m", choices=["m","d","f","o"], help="Estrategia a implementar")
parser.add_argument("-a", default="f", choices=["f","i"], help="Capital")
args = parser.parse_args()
num_tiradas = args.c
num_corridas = args.n
color_elegido = args.e
estrategia = args.s
capital = args.a

opciones_estrategias = ["Martingala","DAlembert","Fibonacci","Paroli"]
if estrategia == "m": estrategia = "Martingala"
if estrategia == "d": estrategia = "DAlembert"
if estrategia == "f": estrategia = "Fibonacci"
if estrategia == "o": estrategia = "Paroli"
opciones_capital = ["Finito","Infinito"]
if capital == "f": capital = "Finito"
if capital == "i": capital = "Infinito"

################################RUTAS################################
# Obtener la ruta completa del directorio
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_graficas = os.path.join(directorio_actual, 'graficas')
ruta_datos = os.path.join(directorio_actual, 'datos_json')
# Verificar si el directorio no existe y crearlo
if not os.path.exists(ruta_graficas):
    os.makedirs(ruta_graficas)
if not os.path.exists(ruta_datos):
    os.makedirs(ruta_datos)


################################PROGRAMA################################             
def programa(): 
    colec_cap_act, colec_frec_positiva = [], []
    opciones_color=['n', 'r', 'v']
    prob=[0.486486, 0.486486, 0.027027]

    for _ in range(num_corridas):
        capital_actual, frec_positiva = [], []
        p, q = 0, 0
        apuesta = 1
        if capital == 'Finito':                #Capital Finito
            capital_inicial = 500
            capital_actual.append(capital_inicial)
            if estrategia == 'Martingala':                #Martingala
                for _ in range(num_tiradas):
                    if capital_inicial > apuesta:
                        resultado = random.choices(opciones_color, prob)[0]      #funcion que elige (n, r, v) con probabilidades distintas
                        if resultado != color_elegido:
                            capital_inicial -= apuesta
                            apuesta *= 2
                            q+=1
                        if resultado == color_elegido:                        
                            capital_inicial += apuesta
                            apuesta = 1
                            if q >= len(frec_positiva):
                                frec_positiva.extend([0] * (q - len(frec_positiva) + 1))
                            frec_positiva[q]+=1
                            q=0
                        p+=1
                    capital_actual.append(capital_inicial)
                for i in range(len(frec_positiva)):
                    frec_positiva[i] = frec_positiva[i]/p
            elif estrategia == 'DAlembert':              #D'Alembert
                for _ in range(num_tiradas):
                    if capital_inicial > apuesta:
                        resultado = random.choices(opciones_color, prob)[0]
                        if resultado != color_elegido:
                            capital_inicial -= apuesta
                            apuesta += 1
                            q+=1
                        if resultado == color_elegido:
                            capital_inicial += apuesta
                            if apuesta > 1:
                                apuesta -= 1
                            else: apuesta = 1
                            if q >= len(frec_positiva):
                                frec_positiva.extend([0] * (q - len(frec_positiva) + 1))
                            frec_positiva[q]+=1
                            q=0
                        p+=1
                    capital_actual.append(capital_inicial)
                for i in range(len(frec_positiva)):
                    frec_positiva[i] = frec_positiva[i]/p                
            elif estrategia == 'Fibonacci':              #Fibonacci
                i = 0
                sec_fib=[1,1]
                for _ in range(2, 300):
                    sec_fib.append(sec_fib[-1]+sec_fib[-2])
                for _ in range(num_tiradas):
                    if capital_inicial > sec_fib[i]:
                        resultado = random.choices(opciones_color, prob)[0]
                        if resultado != color_elegido:
                            capital_inicial -= sec_fib[i]
                            i+=1
                            q+=1
                        if resultado == color_elegido:
                            capital_inicial += sec_fib[i]
                            if i<=2:
                                i=0
                            else: i-=2
                            if q >= len(frec_positiva):
                                frec_positiva.extend([0] * (q - len(frec_positiva) + 1))
                            frec_positiva[q]+=1
                            q=0
                        p+=1
                    capital_actual.append(capital_inicial)
                for i in range(len(frec_positiva)):
                    frec_positiva[i] = frec_positiva[i]/p        
            elif estrategia == 'Paroli':              #Paroli
                i = 0
                for _ in range(num_tiradas):
                    if capital_inicial > apuesta:
                        resultado = random.choices(opciones_color, prob)[0]
                        if resultado != color_elegido:
                            capital_inicial -= apuesta
                            apuesta = 1
                            q+=1
                        if resultado == color_elegido:
                            capital_inicial += apuesta
                            apuesta *= 2
                            i+=1
                            if i==3:
                                apuesta = 1
                                i=0
                            if q >= len(frec_positiva):
                                frec_positiva.extend([0] * (q - len(frec_positiva) + 1))
                            frec_positiva[q]+=1
                            q=0
                        p+=1
                    capital_actual.append(capital_inicial)
                for i in range(len(frec_positiva)):
                    frec_positiva[i] = frec_positiva[i]/p

        elif capital == 'Infinito':                  #Capital Infinito
            capital_inicial = 0
            if estrategia == 'Martingala':                #Martingala
                for _ in range(num_tiradas):
                    resultado = random.choices(opciones_color, prob)[0]
                    if resultado != color_elegido:
                        capital_inicial -= apuesta
                        apuesta *= 2
                        q+=1
                    if resultado == color_elegido:
                        capital_inicial += apuesta
                        apuesta = 1
                        if q >= len(frec_positiva):
                            frec_positiva.extend([0] * (q - len(frec_positiva) + 1))
                        frec_positiva[q]+=1
                        q=0
                    capital_actual.append(capital_inicial)
                    p+=1
                for i in range(len(frec_positiva)):
                    frec_positiva[i] = frec_positiva[i]/p
            elif estrategia == 'DAlembert':              #D'Alembert
                for _ in range(num_tiradas):
                    resultado = random.choices(opciones_color, prob)[0]
                    if resultado != color_elegido:
                        capital_inicial -= apuesta
                        apuesta += 1
                        q+=1
                    if resultado == color_elegido:
                        capital_inicial += apuesta
                        if apuesta > 1:
                            apuesta -= 1
                        else: apuesta = 1
                        if q >= len(frec_positiva):
                            frec_positiva.extend([0] * (q - len(frec_positiva) + 1))
                        frec_positiva[q]+=1
                        q=0
                    capital_actual.append(capital_inicial)
                    p+=1
                for i in range(len(frec_positiva)):
                    frec_positiva[i] = frec_positiva[i]/p
            elif estrategia == 'Fibonacci':              #Fibonacci
                i = 0
                sec_fib=[1,1]
                for t in range(2, 10000):
                    sec_fib.append(sec_fib[t-1]+sec_fib[t-2])
                for _ in range(num_tiradas):
                    resultado = random.choices(opciones_color, prob)[0]
                    if resultado != color_elegido:
                        capital_inicial -= sec_fib[i]
                        i+=1
                        q+=1
                    if resultado == color_elegido:
                        capital_inicial += sec_fib[i]
                        if i<=2:
                            i=0
                        else: i-=2
                        if q >= len(frec_positiva):
                            frec_positiva.extend([0] * (q - len(frec_positiva) + 1))
                        frec_positiva[q]+=1
                        q=0
                    capital_actual.append(capital_inicial)
                    p+=1
                for i in range(len(frec_positiva)):
                    frec_positiva[i] = frec_positiva[i]/p        
            elif estrategia == 'Paroli':              #Paroli
                i = 0
                for _ in range(num_tiradas):
                    resultado = random.choices(opciones_color, prob)[0]
                    if resultado != color_elegido:
                        capital_inicial -= apuesta
                        apuesta = 1
                        q+=1
                    if resultado == color_elegido:
                        capital_inicial += apuesta
                        apuesta *= 2
                        if q >= len(frec_positiva):
                            frec_positiva.extend([0] * (q - len(frec_positiva) + 1))
                        frec_positiva[q]+=1
                        q=0
                    i+=1
                    if i==3:
                        apuesta = 1
                        i=0
                    capital_actual.append(capital_inicial)
                    p+=1
                for i in range(len(frec_positiva)):
                    frec_positiva[i] = frec_positiva[i]/p
        
        colec_cap_act.append(capital_actual)  #Para guardar los valores de capital_actual en cada corrida
        colec_frec_positiva.append(frec_positiva)  #Para guardar los valores de frec_positiva en cada corrida
    return colec_cap_act, colec_frec_positiva

def graficar(colec_cap_act, colec_frec_positiva, numero = -1):
    plt.figure()
    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    if numero == -1:
        for i in range(len(colec_cap_act)):
            plt.plot(colec_cap_act[i], label=f'Corrida {i+1}')
    elif numero >= 0 and numero < len(colec_cap_act):
        plt.plot(colec_cap_act[numero], label=f'Corrida {numero+1}')
    if capital == 'Infinito':
        t=[0 for _ in range(num_tiradas)]
        plt.plot(t, label='Capital Inicial', linestyle='--', color='black')
    if capital == 'Finito':
        t=[500 for _ in range(num_tiradas)]
        plt.plot(t, label='Capital Inicial', linestyle='--', color='black')    
    plt.title("Capital vs Tiradas")
    plt.xlabel("Tiradas")
    plt.ylabel("Capital")
    plt.tight_layout()
    plt.legend()
    grafico_1 = os.path.join(ruta_graficas, f'flujo_caja_{estrategia}_{capital}.png')
    plt.savefig(grafico_1)

    plt.figure()
    fig = plt.gcf()
    fig.set_size_inches(10, 10)
    for i in range(len(colec_frec_positiva)):
        x = np.arange(len(colec_frec_positiva[i]))
        plt.bar(x, colec_frec_positiva[i], width=1, edgecolor="black", linewidth=0.7, alpha=0.2, label=f'Corrida {i+1}')
    plt.title(f"Frecuencia de ganancia")
    plt.xlabel("Tiradas")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.legend()
    grafico_2 = os.path.join(ruta_graficas, f'frecuencia_numeros_{estrategia}_{capital}.png')
    plt.savefig(grafico_2)

###############################HACER TODOS LOS CASOS################################
for elegir_capital in range(2):
    capital = opciones_capital[elegir_capital]
    for elegir_estrategia in range(4):       
        estrategia = opciones_estrategias[elegir_estrategia]
        colec_cap_act, colec_frec_positiva = programa()
        #sacar promedio de colec_cap_act y colec_frec_positiva
        promedio_cap_act = [sum(x)/len(x) for x in zip(*colec_cap_act)]
        promedio_frec_positiva = [sum(x)/len(x) for x in zip(*colec_frec_positiva)]
        
        
        ruta_archivo = os.path.join(ruta_datos, f'listas_{estrategia}_{capital}.json')
        with open(ruta_archivo, 'w') as jf: 
            json.dump([colec_cap_act, colec_frec_positiva], jf, ensure_ascii=False, indent=2)
        
        ruta_archivo = os.path.join(ruta_datos, f'promedios_{estrategia}_{capital}.json')
        with open(ruta_archivo, 'w') as jf: 
            json.dump([promedio_cap_act, promedio_frec_positiva], jf, ensure_ascii=False, indent=2)
        
        graficar(colec_cap_act, colec_frec_positiva)
        graficar([promedio_cap_act], [promedio_frec_positiva], 0)
