import snap
import urllib.request
import os
import matplotlib.pyplot as plt
import time
import heapq
import networkx as nx
import numpy as np

# URL do dataset da rede social do Facebook
dataset_url = 'https://snap.stanford.edu/data/facebook_combined.txt.gz'
compressed_filename = 'facebook_combined.txt.gz'
uncompressed_filename = 'facebook_combined.txt'

# Baixa o dataset se ele não existir localmente
if not os.path.isfile(compressed_filename):
    print('Baixando o dataset...')
    urllib.request.urlretrieve(dataset_url, compressed_filename)
    print('Download concluído.')

# Descompacta o arquivo se não existir
if not os.path.isfile(uncompressed_filename):
    print('Descompactando o dataset...')
    import gzip
    # Abri o arquivo compactado (.gz) e salva o conteúdo em um novo arquivo (.txt)
    with gzip.open(compressed_filename, 'rb') as f_in:
        with open(uncompressed_filename, 'wb') as f_out:
            f_out.write(f_in.read())
    print('Descompactação concluída.')

# Carrega o grafo utilizando o SNAP (grafo não direcionado)
print('Carregando o grafo...')
G = snap.LoadEdgeList(snap.PUNGraph, uncompressed_filename, 0, 1)
print('Grafo carregado.')

# Imprime o total de nós (perfis) e arestas (amizades)
total_nodes = G.GetNodes()
total_edges = G.GetEdges()
print(f'Total de nós: {total_nodes}')
print(f'Total de arestas: {total_edges}')

# Converte o grafo SNAP para um grafo NetworkX para fins de visualização
G_nx = nx.Graph()
for EI in G.Edges():
    G_nx.add_edge(EI.GetSrcNId(), EI.GetDstNId())

# Seleciona um nó de origem para calcular os menores caminhos
source_node = G.BegNI().GetId()  # Seleciona o primeiro nó do grafo como nó de origem
print('Nó de origem:', source_node)

# Implementação do Algoritmo de Dijkstra usando uma fila de prioridade (heapq)
def dijkstra_all_nodes(G, source):
    # Inicializar todas as distâncias como infinito
    distances = {node.GetId(): float('inf') for node in G.Nodes()}
    distances[source] = 0  # Distância do nó de origem para ele mesmo é 0
    visited = set()  # Conjunto de nós já visitados
    heap = [(0, source)]  # Fila de prioridade com (custo, nó)

    while heap:
        (cost, u) = heapq.heappop(heap)  # Remove o nó com menor custo da fila
        if u in visited:
            continue  # Ignorar se já foi visitado
        visited.add(u)  # Marcar nó como visitado
        NI = G.GetNI(u)  # Obter informações do nó atual

        # Percorrer os nós adjacentes
        for i in range(NI.GetOutDeg()):
            v = NI.GetOutNId(i)  # Nó vizinho
            if v not in visited:
                new_cost = cost + 1  # Peso da aresta é 1 (grafo não ponderado)
                if new_cost < distances[v]:
                    distances[v] = new_cost  # Atualizar menor custo encontrado
                    heapq.heappush(heap, (new_cost, v))  # Adicionar nó à fila com o novo custo

    return distances

# Executar o algoritmo de Dijkstra otimizado
print('Executando o algoritmo de Dijkstra otimizado...')
start_time = time.time()
distances_dijkstra_optimized = dijkstra_all_nodes(G, source_node)
optimized_dijkstra_time = time.time() - start_time
print('Dijkstra otimizado concluído em {:.2f} segundos.'.format(optimized_dijkstra_time))

# Implementação do Algoritmo de Bellman-Ford
print('Executando o algoritmo de Bellman-Ford...')
start_time = time.time()
# Inicializar as distâncias com infinito
distances_bellman_ford = {node.GetId(): float('inf') for node in G.Nodes()}
distances_bellman_ford[source_node] = 0  # Distância do nó de origem é zero

# Relaxar as arestas |V| - 1 vezes, onde |V| é o número de nós
for _ in range(G.GetNodes() - 1):
    updated = False  # Controle de atualizações
    # Percorrer todas as arestas do grafo
    for EI in G.Edges():
        u = EI.GetSrcNId()
        v = EI.GetDstNId()
        weight = 1  # Peso da aresta
        # Relaxamento das arestas (atualizar distâncias)
        if distances_bellman_ford[u] + weight < distances_bellman_ford[v]:
            distances_bellman_ford[v] = distances_bellman_ford[u] + weight
            updated = True
        if distances_bellman_ford[v] + weight < distances_bellman_ford[u]:
            distances_bellman_ford[u] = distances_bellman_ford[v] + weight
            updated = True
    if not updated:
        break  # Se não houver atualizações, sair do loop
bellman_ford_time = time.time() - start_time
print('Bellman-Ford concluído em {:.2f} segundos.'.format(bellman_ford_time))

# Comparar os resultados dos dois algoritmos
same_results = distances_dijkstra_optimized == distances_bellman_ford
print("Dijkstra otimizado e Bellman-Ford produzem os mesmos resultados:", same_results)

# Visualização de uma parte do grafo: Subgrafo com os primeiros 100 nós
nodes_subset = list(G_nx.nodes())[:100]  # Selecionar os primeiros 100 nós
subgraph = G_nx.subgraph(nodes_subset)

# Plotar o subgrafo
plt.figure(figsize=(12, 8))
nx.draw_networkx(
    subgraph,
    with_labels=False,
    node_size=50,
    node_color='blue',
    edge_color='gray'
)
plt.title('Visualização de um Subgrafo do Grafo Facebook')
plt.show()

# Plotar a distribuição do grau dos nós
degrees = [val for (node, val) in G_nx.degree()]  # Obter o grau de cada nó
plt.figure(figsize=(10, 6))
plt.hist(degrees, bins=range(max(degrees) + 1), edgecolor='black', log=True)
plt.title('Distribuição do Grau dos Nós')
plt.xlabel('Grau')
plt.ylabel('Frequência (escala logarítmica)')
plt.show()

# Plotar a distribuição dos comprimentos dos caminhos mais curtos
path_lengths = list(distances_dijkstra_optimized.values())
plt.figure(figsize=(10, 6))
plt.hist(
    path_lengths,
    bins=range(int(max(path_lengths)) + 1),
    align='left',
    edgecolor='black'
)
plt.title(
    'Distribuição dos Comprimentos dos Caminhos Mais Curtos a partir do Nó {}'.format(
        source_node
    )
)
plt.xlabel('Comprimento do Caminho Mais Curto')
plt.ylabel('Número de Nós')
plt.xticks(range(int(max(path_lengths)) + 1))
plt.show()

# Comparação dos tempos de execução dos algoritmos
plt.figure(figsize=(8, 6))
algorithms = ['Dijkstra Otimizado', 'Bellman-Ford']
times = [optimized_dijkstra_time, bellman_ford_time]
colors = ['skyblue', 'lightgreen']

plt.bar(algorithms, times, color=colors, edgecolor='black')
plt.ylabel('Tempo de Execução (segundos)')
plt.title('Comparação dos Tempos de Execução dos Algoritmos')
for i, v in enumerate(times):
    plt.text(i, v + 0.05, f"{v:.2f}s", ha='center', fontweight='bold')
plt.show()

# Plotar a distribuição da centralidade de intermediação dos nós (betweenness centrality)
centrality = nx.betweenness_centrality(G_nx)
plt.figure(figsize=(10, 6))
plt.hist(list(centrality.values()), bins=50, edgecolor='black', log=True)
plt.title('Distribuição da Centralidade de Intermediação dos Nós')
plt.xlabel('Centralidade de Intermediação')
plt.ylabel('Frequência (escala logarítmica)')
plt.show()

# Plotar a distribuição dos coeficientes de agrupamento dos nós
degrees_clustering = nx.clustering(G_nx)
plt.figure(figsize=(10, 6))
plt.hist(list(degrees_clustering.values()), bins=50, edgecolor='black', log=True)
plt.title('Distribuição dos Coeficientes de Agrupamento dos Nós')
plt.xlabel('Coeficiente de Agrupamento')
plt.ylabel('Frequência (escala logarítmica)')
plt.show()

# Plotar a distribuição dos tamanhos dos componentes conexos
connected_components = [len(c) for c in sorted(nx.connected_components(G_nx), key=len, reverse=True)]
plt.figure(figsize=(10, 6))
plt.hist(connected_components, bins=50, edgecolor='black', log=True)
plt.title('Distribuição dos Tamanhos dos Componentes Conexos')
plt.xlabel('Tamanho do Componente Conexo')
plt.ylabel('Frequência (escala logarítmica)')
plt.show()

# Plotar o mapa de calor da matriz de adjacência do grafo
adj_matrix = nx.to_numpy_array(G_nx)
plt.figure(figsize=(10, 8))
plt.imshow(adj_matrix, cmap='hot', interpolation='nearest')
plt.title('Mapa de Calor da Matriz de Adjacência')
plt.xlabel('Nós')
plt.ylabel('Nós')
plt.colorbar()
plt.show()
