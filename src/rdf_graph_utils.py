import os
from time import time
import networkx as nx
import matplotlib.pyplot as plt
import shlex
import statistics


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

# gestione numero predicato-oggetto significativi
def pred_obj_significant(directory, iteration, gp):
    outputnt = open(directory + '/output_tmp_LCS_' + str(iteration) + '.nt', 'r')
    outputifirstlv =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_first_lv.nt', 'a')
    outputisecondtlv =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_second_lv.nt', 'a')
    filecountfirst = 0
    filecountsecond = 0
    row = 0
    secondlvfound = False
    temparrayfirst = []
    temparraysecond = []

    for line in outputnt.readlines():
          line = line.replace('<', '').replace('>', '')
          s, p, o, _ = shlex.split(line)
          if row == 0:
            firstlv = s
            row += 1
          elif s != firstlv and secondlvfound == False:
            secondlv = s
            secondlvfound = True
          if s == firstlv:
            triplecheck(s, p, o, _, gp, temparrayfirst, outputifirstlv)           
          elif s == secondlv:
            triplecheck(s, p, o, _, gp, temparraysecond, outputisecondtlv)

    outputifirstlv.close()
    outputisecondtlv.close()
    outputnt.close()

    filecountfirst, filecountsecond = triplecount(directory, iteration)

    return filecountfirst, filecountsecond

# controllo delle triple
def triplecheck(s, p, o, _, gp, temparray, outputfile):
    if not ('_:blank_' in p) and not ('_:blank_' in o) and ('http' in o):
                for goodline in gp:
                  if goodline == p:
                      tempstring = s + ' ' + p + ' ' + o + ' ' + _
                      if not (tempstring in temparray):
                        temparray.append(tempstring)
                        outputfile.write(s + ' ' + p + ' ' + o + ' ' + _ + ' ' + '\n')

# count triple
def triplecount(directory, iteration):
    outputifirstlv =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_first_lv.nt', 'r')
    outputisecondtlv =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_second_lv.nt', 'r')

    filecountfirst = len(outputifirstlv.readlines())
    filecountsecond = len(outputisecondtlv.readlines())

    outputifirstlv.close()
    outputisecondtlv.close()
    
    return filecountfirst, filecountsecond

# valutazione con iterazione precedente
def prev_iteration_evaluation(iteration, graph_1, explored_resoures_ok, resource_2, file, directory, filecountfirst, filecountsecond, graph_ok):
    stop = False
    if iteration == 0:
        graph_ok = graph_1
        explored_resoures_ok.append(resource_2)
        file.write("Iterazione: " + str(iteration) +  " risorse esplorate: " + str(explored_resoures_ok) + "\n")

    if iteration != 0:
        prevfilecountfirst, prevfilecountsecond = triplecount(directory, iteration - 1)
        arrcur = [filecountfirst, filecountsecond]
        arrprev = [prevfilecountfirst, prevfilecountsecond]
        mediancurr = statistics.median(arrcur)
        medianprev = statistics.median(arrprev)
        print('Current median: ', mediancurr)
        print('Previous median: ', medianprev)
        # statistics.variance()
        # statistics.stdev()
        if medianprev <= mediancurr:
            graph_ok = graph_1
            explored_resoures_ok.append(resource_2)
            file.write("Iterazione: " + str(iteration) +  " risorse esplorate: " + str(explored_resoures_ok) + "\n")
        else:
            stop = True
            print("Iteration stopped at iteration: " + str(iteration))

    return graph_ok, explored_resoures_ok, stop                     
