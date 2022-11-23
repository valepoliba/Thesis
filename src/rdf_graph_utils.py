import os
from time import time
import networkx as nx
import matplotlib.pyplot as plt
import shlex
import difflib


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
    outputietration =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant.nt', 'a')
    outputietration_temp =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_temp.nt', 'a')
    outputietration_temp2 =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_temp2.nt', 'a')
    filecount = 0
    for line in outputnt.readlines():
          line = line.replace('<', '').replace('>', '')
          s, p, o, _ = shlex.split(line)
          if not ('_:blank_' in p) and not ('_:blank_' in o) and ('http' in o):
                for goodline in gp:
                  if goodline == p:
                      outputietration.write(s + ' ' + p + ' ' + o + ' ' + _ + ' ' + '\n')
                      outputietration_temp.write(p + ' ' + o + ' ' + _ + ' ' + '\n')
                      outputietration_temp2.write(p + '\n')
                      filecount += 1
    print('Count significant row: ', filecount)
    outputietration.close()
    outputnt.close()
    outputietration_temp.close()
    outputietration_temp2.close()

# confronto con iterazione precedente dei po significativi
def compare_prev_next_iteration(directory, iteration):
    diffcheck = False
    if iteration != 0:  
      with open(directory + '/output_tmp_LCS_' + str(iteration-1) + '_po_significant_temp.nt') as po1:
            po_1 = po1.readlines()
      
      with open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_temp.nt') as po2:
            po_2 = po2.readlines()

      outputietrationdifference =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_difference.nt', 'a')
      
      # Find and print the diff:
      for line in difflib.unified_diff(po_1, po_2, fromfile=str(po1), tofile=str(po2), lineterm='', n=0):
            diffcheck = True
            outputietrationdifference.write(line + '\n')

      if diffcheck == False:
            outputietrationdifference.write('NO DIFFERENCE WAS FOUND')

      outputietrationdifference.close()
      po1.close()
      po2.close()
      os.remove(directory + '/output_tmp_LCS_' + str(iteration-1) + '_po_significant_temp.nt')  

# numero predicati diversi
def different_predicates_count(directory, iteration):
    outputnt = open(directory + '/output_tmp_LCS_' + str(iteration) + '.nt', 'r')
    outputietration =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_different_predicates.nt', 'a')
    temparray = []

    for line in outputnt.readlines():
            line = line.replace('<', '').replace('>', '')
            s, p, o, _ = shlex.split(line)
            if not (p in temparray):
                temparray.append(p)
                
    print('Different predicates count: ' + str(len(temparray)))
    outputietration.write(str('\n'.join(temparray)) + '\n')
    # outputietration.write('\n' + '#######' + '\n' + 'Different predicates count: ' + str(len(temparray)))
    outputietration.close()
    outputnt.close()

# differenza predicati - significativi
def diff_pred_significant(directory, iteration):
    with open(directory + '/output_tmp_LCS_' + str(iteration) + '_different_predicates.nt') as po1:
        po_1 = po1.readlines()
      
    with open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_temp2.nt') as po2:
        po_2 = po2.readlines()

    outputietrationdifference =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_predicate_difference.nt', 'a')
    diffcheck = False  
    # Find and print the diff:
    for line in difflib.unified_diff(po_1, po_2, fromfile=str(po1), tofile=str(po2), lineterm='', n=0):
        diffcheck = True
        outputietrationdifference.write(line + '\n')

    if diffcheck == False:
        outputietrationdifference.write('NO DIFFERENCE WAS FOUND')

    outputietrationdifference.close()
    po1.close()
    po2.close()
    os.remove(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant_temp2.nt')

