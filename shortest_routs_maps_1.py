from flask import Flask, render_template, request, send_file
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

app = Flask(__name__)

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
    df = pd.read_csv(csv_path)
    graph = {}
    for _, row in df.iterrows():
        if row['source'] not in graph:
            graph[row['source']] = {}
        graph[row['source']][row['target']] = row['weight']
    return graph

def draw_with_shortest_path(maps, shortest_path):
    g = nx.DiGraph()
    color = []

    for source, targets in maps.items():
        for target, weight in targets.items():
            g.add_edge(source, target, weight=str(weight) + " km")

    pos = nx.shell_layout(g)
    edge_labels = {(u, v): d['weight'] for u, v, d in g.edges(data=True)}

    # Highlight edges in the shortest path with a different color
    edge_colors = ['red' if (u, v) in zip(shortest_path, shortest_path[1:]) else 'gray' for u, v in g.edges()]

    # Generate plot dynamically and save to BytesIO buffer
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(g, pos, node_size=1000, node_color=color, ax=ax)
    nx.draw_networkx_edges(g, pos, edgelist=g.edges(), edge_color=edge_colors, ax=ax)
    nx.draw_networkx_labels(g, pos, ax=ax)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, ax=ax)
    ax.set_title("MAPS")
    ax.axis("off")

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close(fig)

    return img_buffer

#     return img_buffer
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_route', methods=['POST'])
def show_route():
    csv_path = request.form['csv_path']
    source_node = request.form['source_node']
    destination_node = request.form['destination_node']

    maps = load_graph_from_csv(csv_path)
    shortest_path = shortest(maps, source_node, destination_node)
    img_buffer = draw_with_shortest_path(maps, shortest_path)

    return render_template('show_route.html', shortest_path=shortest_path, img_buffer=base64.b64encode(img_buffer.getvalue()).decode('utf-8'))

@app.route('/get_image')
def get_image():
    img_buffer = BytesIO(request.args.get('img_buffer', None))
    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
