# Diário

## O que esperávamos antes de medir

- **Insertion Sort, entrada aleatória:** esperávamos que fosse o pior caso da
  medição, com o tempo crescendo muito rápido ao aumentar n, já que cada
  elemento pode precisar ser deslocado por boa parte da lista.
- **Insertion Sort, entrada ordenada:** esperávamos que fosse bem mais rápido,
  porque o `while` quase não executaria. Chutamos uma diferença de umas 100
  vezes em relação à entrada aleatória.
- **Merge Sort:** esperávamos o mesmo tempo nos dois cenários, já que ele sempre
  divide a lista ao meio, esteja ela ordenada ou não.
- **Comparação entre os dois:** esperávamos que o Merge Sort ganhasse sempre, por
  ter complexidade melhor.
- **Razões ao dobrar n:** esperávamos valores bem próximos do teórico (4 para
  O(n²), 2 para O(n), pouco acima de 2 para O(n log n)).

---

## O que deu errado

### Primeira versão dos testes não seguia o protocolo

Os arquivos `executadorInSort.py` e `executadorMeSort.py` foram as primeiras
versões dos testes. Eles rodavam cada algoritmo uma única vez, com o tamanho
digitado à mão no código (`qntValores`), sem descartar a primeira execução e sem
mediana. Foram substituídos pelo `medir.py` e mantidos como registro.

### Risco de medir o cenário errado

O `inSort` ordena a lista no lugar. Se a mesma lista fosse passada nas 4
execuções, só a primeira ordenaria uma lista aleatória; as outras 3 já receberiam
a lista ordenada, e a mediana mediria o cenário ordenado sem percebermos.
Percebemos isso antes de medir e passamos a usar uma cópia (`lista[:]`) a cada
execução.

### Ruído no Insertion Sort com entrada ordenada

Em n = 8.000 a razão deu 4,68, quando o esperado era cerca de 2. Os tempos desse
cenário são de poucos milissegundos, e pequenas interferências do sistema pesam
proporcionalmente muito. Os tamanhos vizinhos voltaram para perto de 2, então
tratamos o ponto como ruído, e não como mudança de classe.

### Razões do Merge Sort acima do esperado

Para O(n log n), a razão esperada ao dobrar n é cerca de 2,2. Nos tamanhos
menores deu 2,10–2,18, mas em 8.000 e 16.000 subiu para 2,56–3,02. Uma explicação
provável é o custo de memória: o Merge Sort cria muitas listas novas a cada
divisão e junção, e com n grande isso sobrecarrega o cache e o gerenciador de
memória do Python.
