import csv
from pathlib import Path

import matplotlib.pyplot as plt

raiz = Path(__file__).resolve().parent.parent
arquivoCsv = raiz / "dados" / "tempos.csv"
arquivoPng = raiz / "graficos" / "comparacao.png"

# cor = algoritmo, estilo da linha = cenário (não depende só de cor para distinguir)
cores = {"insertion": "#2a78d6", "merge": "#eb6834"}
estilos = {"aleatoria": "-", "ordenada": "--"}
nomes = {"insertion": "Insertion Sort", "merge": "Merge Sort"}

series = {}
with open(arquivoCsv, newline="") as f:
    for linha in csv.DictReader(f):
        chave = (linha["algoritmo"], linha["cenario"])
        series.setdefault(chave, ([], []))
        series[chave][0].append(int(linha["n"]))
        series[chave][1].append(float(linha["mediana_s"]))

fig, ax = plt.subplots(figsize=(9, 5.5))

for (algoritmo, cenario), (ns, tempos) in series.items():
    rotulo = f"{nomes[algoritmo]} ({cenario.replace('aleatoria', 'aleatória')})"
    ax.plot(ns, tempos, estilos[cenario], color=cores[algoritmo], linewidth=2,
            marker="o", markersize=6, label=rotulo)
    # rótulo direto no fim da linha
    ax.annotate(rotulo, (ns[-1], tempos[-1]), xytext=(8, 0), textcoords="offset points",
                va="center", fontsize=9, color="#333333")

# log-log: sem isso o Insertion aleatório esmaga as outras linhas perto do zero
ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.set_xticks(series[("insertion", "aleatoria")][0])
ax.set_xticklabels([str(n) for n in series[("insertion", "aleatoria")][0]])
ax.set_xlim(right=16000 * 3.2)  # espaço para os rótulos à direita

ax.set_title("Tempo de ordenação: entrada aleatória vs. ordenada", loc="left", fontsize=13)
ax.set_xlabel("Tamanho da entrada (n)")
ax.set_ylabel("Tempo mediano (s, escala log)")
ax.grid(True, which="major", color="#e5e5e5", linewidth=0.8)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="upper left")

arquivoPng.parent.mkdir(exist_ok=True)
fig.tight_layout()
fig.savefig(arquivoPng, dpi=150)
print(f"Salvo em {arquivoPng}")
