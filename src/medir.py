import csv
import statistics
import time
from pathlib import Path

from InSort import inSort
from MeSort import meSort
from ListaRand import listaRand, listaOrd

tamanhos = [1000, 2000, 4000, 8000, 16000]
algoritmos = {"insertion": inSort, "merge": meSort}
execucoes = 4  # a primeira é descartada, sobram 3 para a mediana

# dados/ fica na raiz do repositório, um nível acima de src/
arquivoCsv = Path(__file__).resolve().parent.parent / "dados" / "tempos.csv"

resultados = []

for n in tamanhos:
    # mesma lista base para os dois algoritmos: comparação justa
    base = listaRand(n)
    cenarios = {"aleatoria": base, "ordenada": listaOrd(base)}

    for nome, funcao in algoritmos.items():
        for cenario, lista in cenarios.items():
            tempos = []
            for _ in range(execucoes):
                copia = lista[:]  # inSort ordena no lugar; sem cópia a 2ª execução já pegaria lista ordenada
                inicio = time.perf_counter()
                funcao(copia)
                fim = time.perf_counter()
                tempos.append(fim - inicio)

            mediana = statistics.median(tempos[1:])  # descarta a primeira (aquecimento)
            resultados.append([nome, cenario, n, mediana])
            print(f"{nome:<10} {cenario:<10} n={n:<6} mediana={mediana:.6f}s")

# razão = tempo(n) / tempo(n/2) dentro de cada combinação algoritmo+cenário
anterior = {}
for linha in resultados:
    chave = (linha[0], linha[1])
    linha.append(round(linha[3] / anterior[chave], 2) if chave in anterior else "")
    anterior[chave] = linha[3]

arquivoCsv.parent.mkdir(exist_ok=True)
with open(arquivoCsv, "w", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerow(["algoritmo", "cenario", "n", "mediana_s", "razao"])
    escritor.writerows(resultados)

print(f"\nSalvo em {arquivoCsv}")
