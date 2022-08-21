import rdflib
import shlex


def parse(path):
    dict = {}
    with open(path, "r") as file:
        for line in file:
            key, val = line.rstrip("\n").split('" "')
            dict[key.strip('"')] = val.strip('"')

    return dict


def most_conncted(roots, graph):
    counts = {v: 0 for v in roots}
    for root in roots:
        for (s, p, o) in graph:
            if s == root:
                counts[root] += 1

    return max(counts.keys(), key=lambda k: counts[k])


def my_root_node(graph):
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

        # print("multiple root nodes found. ")
        return most_conncted(ss1, graph)
        # raise Exception("Error: multiple root nodes found.")
############################## params ########################################


depth = 2

path = "/home/nico/Uni/Tesi/Tesi/RDF_Clustering/outputs/drugbank/oLast-w-html_lvl1_NQ/output_tmp_LCS_1.nt"

g = rdflib.Graph()

with open(path, "r") as f:
    for line in f.readlines():
        line = line.replace("<", "").replace(">", "")
        if line:
            s, p, o, _ = shlex.split(line)
            if "_:blank_" in s: s = "blank:" + s.replace("_:blank_", "")
            if "_:blank_" in p: p = "blank:" + p.replace("_:blank_", "")
            if "_:blank_" in o: o = "blank:" + o.replace("_:blank_", "")

            if not ("http" in s or "blank:" in s):
                s2 = rdflib.term.Literal(s)
            else:
                s2 = rdflib.term.URIRef(s)

            if not ("http" in p or "blank:" in p):
                p2 = rdflib.term.Literal(p)
            else:
                p2 = rdflib.term.URIRef(p)

            if not ("http" in o or "blank:" in o):
                o2 = rdflib.term.Literal(o)
            else:
                o2 = rdflib.term.URIRef(o)

            g.add((s2, p2, o2))



'''
g = rdflib.Graph()
for s, p, o in t:
    if isinstance(s, rdflib.term.BNode):
        s = rdflib.term.URIRef("blank:" + str(s))

    if isinstance(p, rdflib.term.BNode):
        p = rdflib.term.URIRef("blank:" + str(p))

    if isinstance(o, rdflib.term.BNode):
        o = rdflib.term.URIRef("blank:" + str(o))

    g.add((s, p, o))


'''

root = my_root_node(g)

# root = "blank:efaa98c0d394121979c8e010172cd71b"

preds_dict = parse("drugbank_parameters/predicates_tl.txt")

obj_dicts = parse("drugbank_parameters/objects_tl.txt")


blank_nodes = []
with open("drugbank_parameters/blank_nodes_tl.txt", "r") as file:
    for line in file:
        blank_nodes.append(line.strip('"').strip("\n"))


blank_node_in_output = False

################################################################################################

to_explore = [root]
explored = []
neighbours = []
relative_start = {}
relative_end = {}
output = {}
prop_counter = 1


for iteration in range(depth):
    lvl_output = {}
    lvl_node_number = len(to_explore)
    node_counter = 0
    for node in to_explore:
        node_output = {}
        """ get graph with root node """

        query = """ CONSTRUCT { <?s> ?p ?o. }
                    WHERE { <?s> ?p ?o. }
                """.replace("?s", "%s" % node)



        q_result = g.query(query)
        query_ans = rdflib.Graph()


        for triple in q_result:
            query_ans.add(triple)

        """ if node has no neighbour skip """

        if len(query_ans) < 1: continue
        node_counter += 1
        # manage the subject of the triples
        """ if node is root we are at level one, otherwise we are at level 2+ """
        '''
        if node == root:
            # output += "The resources in the cluster have the following properties in common: \n"
            identif = str(iteration+1)
        else:
            if "blank:" in str(node):

                # output += "the objects referenced before in " \
                #          + bnode_id[str(node)] +  ") present the following properties in common in the cluster: \n"
                identif = str(iteration+1) + "-" + str(bnode_number)
                bnode_number += 1

            else:
                """ resource of lvl 2 is not a blank -> it's a URL (literals are skipped) with properties """
                # output += "the objects referenced before present the following properties in common in the cluster: \n"
                pass
        '''

        prop_counter = 1
        neighbours = []
        explored.append(str(node))

        for (_, p, o) in query_ans:

            # manage remaning sentence of the triples
            if str(p) in preds_dict.keys():
                if str(o) in obj_dicts.keys():
                    node_output["p" + str(prop_counter)] = preds_dict[str(p)] + " \"" + obj_dicts[str(o)].strip() + "\""

                    prop_counter += 1

                elif any(blank_node in str(o) for blank_node in blank_nodes) and blank_node_in_output:
                    node_output["p" + str(prop_counter)] = "They share the property \"" \
                                                           + preds_dict[str(p)]\
                                                               .replace(" is", "")\
                                                               .replace(":", "")\
                                                               .replace("They", "")\
                                                               .replace("Their", "") \
                                                               .strip()\
                                                           + " "  \
                                                           + "\", all of them referencing the same resource " \
                                                             "not further described in the dataset"

                    relative_start[str(o)] = str(iteration + 1) + ":" + str(node_counter) + ":p" + str(prop_counter)
                    prop_counter += 1

                elif "http" not in o and blank_node_in_output:
                    node_output["p" + str(prop_counter)] = "They share the property \"" \
                                                           + preds_dict[str(p)]\
                                                               .replace(" is", "")\
                                                               .replace(":", "") \
                                                               .replace("They", "") \
                                                               .replace("Their", "") \
                                                               .strip() \
                                                           + "\" each one of them referencing some resource"

                    # relative_start[str(o)] = [iteration + 1, node_counter, "p" + str(prop_counter)]
                    relative_start[str(o)] = str(iteration + 1) + ":" + str(node_counter) + ":p" + str(prop_counter)

                    prop_counter += 1

                neighbours.append(o)

                lvl_output[node_counter] = node_output


                if iteration > 0 and str(node) in relative_start.keys():
                    # relative_end[str(node)] = node_output
                    # relative_end[str(node)] = str(iteration + 1) + ":" + str(node_counter) + ":p" + str(prop_counter)
                    for preps in node_output.keys():
                        relative_end[str(iteration + 1) + ":" + str(node_counter) + ":" + preps] = str(node)





    to_explore = [res for res in neighbours if str(res) not in explored]

    output[iteration + 1] = lvl_output
    # print(to_explore)


def adjust_predicate(trad):
    """ replacing third person plural with third person singular  """
    t = trad.replace(" each one of them ", " ")\
        .replace("They", "")\
        .replace(" are ", " is ")\
        .replace(" have ", " has ")\
        .replace("Their property", "has the property")\
        .replace("Their ", " ")\
    # .replace(":", " is ")
    if ":" in t and "\"" not in t:
        fr1, fr2 = t.split(":", 1)
        fr1 = fr1 + " \""
        fr2 = fr2.strip() + "\""
        t = fr1 + fr2
    # t = trad.replace("Their", "has the")
    return t


def get_preposition(out, full_key):
    """ given the key get the preposition from output """
    key_depth, key_node, key_prep = full_key.split(":")
    return out[int(key_depth)][int(key_node)][key_prep]


def relative_explore_recursive(key, output):
    """ build relative preposition in a recursive way """
    result = ""
    if not key in relative_union.values():
        return result
    else:
        result += "\n\t which "
        for succ_key in relative_union.keys():
            if relative_union[succ_key] == key:
                """ recursion """
                result += adjust_predicate(get_preposition(output, succ_key))
                result += relative_explore_recursive(succ_key, output)
                result += "\n\t and "

        return result[:-4]


relative_union = {}
for key_e in relative_end.keys():
    for key_s in relative_start.keys():
        if key_s == relative_end[key_e]:
            relative_union[key_e] = relative_start[key_s]

"""
output[3] = {1: {"p1": "lol", "p2": "lal"}}
relative_union["3:1:p1"] = "2:2:p1"
relative_union["3:1:p2"] = "2:2:p1"
"""

# print(relative_union)
# print(output)

final_output = "The resources in analysis present the following properties in common: \n\n"
output_lvl_1 = output[1][1]
prep_lvl_1_counter = 0
for prep in output_lvl_1:
    prep_lvl_1_counter += 1
    key = "1:1:" + prep
    final_output += str(prep_lvl_1_counter) + ") " + get_preposition(output, key)
    final_output += relative_explore_recursive(key, output)
    final_output += "\n"

print(final_output)
