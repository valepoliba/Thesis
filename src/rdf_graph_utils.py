import os
from time import time
import networkx as nx
import matplotlib.pyplot as plt


def rdf_to_plot(graph, dir):
    print("#### plotting graph ####")
    nx_graph = nx.DiGraph()
    plt.figure(figsize=(50, 50))

    for (s, p, o) in graph:
        s_n = s.split('/')[-1]
        p_n = p.split('/')[-1]
        o_n = o.split('/')[-1]

        nx_graph.add_node(s_n, name=s_n, pred=False)
        nx_graph.add_node(o_n, name=o_n, pred=False)
        nx_graph.add_edge(s_n, o_n, name=p_n)

    pos = nx.spring_layout(nx_graph)
    edge_labels = nx.get_edge_attributes(nx_graph, 'name')
    nx.draw_networkx_nodes(nx_graph, pos=pos)
    nx.draw_networkx_edges(nx_graph, pos=pos)
    nx.draw_networkx_labels(nx_graph, pos=pos, font_size=15)
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_size=12)

    plt.savefig(dir + "/Graph.png", format="PNG")
    plt.show()


# funzione per stampare file
def rdf_to_text(graph, path, format, name):
    # file = "output_" + str(int(time())) + '.' + format
    file = "output_" + name + '.' + format
    path = os.path.join(path, file)

    strings = graph.serialize(format=format)
    with open(path, 'w') as f:
        f.write(strings)


def most_conncted(roots, graph):
    counts = {v: 0 for v in roots}
    for root in roots:
        for (s, p, o) in graph:
            if s == root:
                counts[root] += 1

    return max(counts.keys(), key=lambda k: counts[k])


# estrae root node dal graph rdflib
def root_node(graph):
    ss = set()
    oo = set()
    for (s, p, o) in graph:
        ss.add(s)
        oo.add(p)
        oo.add(o)


    ss1 = ss.difference(oo)
    if len(ss1) == 0:
        raise Exception("Error: no root node found.")
        # return most_conncted(ss, graph)
    elif len(ss1) == 1:
        return ss1.pop()
    else:

        print("multiple root nodes found. ")
        # return most_conncted(ss1, graph)
        raise Exception("Error: multiple root nodes found.")

