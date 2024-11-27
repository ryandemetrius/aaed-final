
# Comparação dos Algoritmos Bellman-Ford e Dijkstra na Busca do Caminho Mais Curto

Esse código é utilizado como base no artigo escrito para o Trabalho Final da Disciplina Isolada de Mestrado - Análise de Algoritmos e Estruturas de Dados - da Universidade Federal de São Paulo - UNIFESP.


## Referências

 - [SNAP - Stanford Network Analysis Project](https://snap.stanford.edu/)
 - [Snap.py - SNAP for Python](https://snap.stanford.edu/snappy/index.html)
 - [SNAP - Facebook Friends Anonymized Dataset](https://snap.stanford.edu/data/ego-Facebook.html)


## Stack utilizada

- Python 3.8.10

- Bibliotecas:

    ``matplotlib``

    ``networkx``

    ``numpy``

    ``snap-stanford (Stanford Network Analysis Platform)``

    ``heapq``

## O Projeto
Esse projeto contém basicamente dois arquivos:
| Nome do arquivo               | Função                                                |
| ----------------- | ---------------------------------------------------------------- |
| main.py       | O código de fato. |
| requirements.txt       | Pacotes necessários para executar o código. |

Os pacotes podem ser instalados com o comando ``pip install -r requirements.txt`` dentro da pasta do projeto.
## O Código (main.py)
O objetivo principal deste projeto é explorar a rede social do Facebook por meio de algoritmos de grafo, gerando insights à partir dos perfis e suas conexões. Utiliza as técnicas de busca de caminho mínimo (Dijkstra e Bellman-Ford), visualizações de subgrafos, análise das distribuições do grau dos nós, dos coeficientes de agrupamento e mapa de calor da matriz de adjacência dos grafos.
