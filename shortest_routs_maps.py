#Shortest_delivery_route


import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def shortest(maps, asal, tujuan):
    result = []
    result.append(asal)

    while tujuan not in result:
        current_node = result[-1]
        jarak_terpendek = min(maps[current_node].values())

        for node, jarak in maps[current_node].items():
            if jarak == jarak_terpendek:
                result.append(node)

    return result

def load_graph_from_csv(csv_path):
    df = pd.read_csv(csv_path)  # Tambahkan csv_path sebagai argumen
    graph = {}
    for _, row in df.iterrows():
        if row['source'] not in graph:
            graph[row['source']] = {}
        graph[row['source']][row['target']] = row['weight']
    return graph

def draw(maps):
    g = nx.DiGraph()
    color = []

    for source, targets in maps.items():
        for target, weight in targets.items():
            g.add_edge(source, target, weight=str(weight) + " km")

    pos = nx.shell_layout(g)
    edge_labels = {(u, v): d['weight'] for u, v, d in g.edges(data=True)}
    nx.draw_networkx_nodes(g, pos, node_size=1000, node_color=color)
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    plt.title("MAPS")
    plt.axis("off")
    plt.show()

def _main():
    csv_path = input("Masukkan path ke file CSV: ")
    maps = load_graph_from_csv(csv_path)


    print("Graf dari CSV:")
    print(maps)

    draw(maps)

    source_node = input("Masukkan node sumber: ")
    destination_node = input("Masukkan node tujuan: ")

    shortest_path = shortest(maps, source_node, destination_node)
    print(f"\nJalur terpendek dari '{source_node}' ke '{destination_node}': {shortest_path}")

if __name__ == '__main__':
    _main()


