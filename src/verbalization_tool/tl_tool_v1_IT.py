import rdflib
from rdf_graph_utils import root_node
import shlex

def parse(path):
    dict = {}
    with open(path, "r") as file:
        for line in file:
            key, val = line.rstrip("\n").split('" "')
            dict[key.strip('"')] = val.strip('"')

    return dict


###

############################## params ########################################

depth = 2

path = "/home/nico/Uni/Tesi/Tesi/RDF_Clustering/results/IT/run3/oAccounts_cluster_6-4_reduced_dbpedia/output_final_LCS.nt"

g = rdflib.Graph()

with open(path, "r") as f:
    for line in f.readlines():
        line = line.replace("<", "").replace(">", "")
        if line:
            s, p, o, _ = shlex.split(line)
            if "_:blank_" in s: s = "blank:" + s.replace("_:blank_", "")
            if "_:blank_" in p: p = "blank:" + p.replace("_:blank_", "")
            if "_:blank_" in o: o = "blank:" + o.replace("_:blank_", "")

            g.add((rdflib.term.URIRef(s),
                   rdflib.term.URIRef(p),
                   rdflib.term.URIRef(o)))


"""
g = rdflib.Graph()
for s, p, o in t:
    if isinstance(s, rdflib.term.BNode):
        s = rdflib.term.URIRef("blank:" + str(s))

    if isinstance(p, rdflib.term.BNode):
        p = rdflib.term.URIRef("blank:" + str(p))

    if isinstance(o, rdflib.term.BNode):
        o = rdflib.term.URIRef("blank:" + str(o))

    g.add((s, p, o))
"""

root = root_node(g)

preds_dict = parse("IT_params/predicates_tl.txt")

obj_dicts = parse("IT_params/objects_tl.txt")


blank_nodes = []
with open("IT_params/blank_nodes_tl.txt", "r") as file:
    for line in file:
        blank_nodes.append(line.strip('"').strip("\n"))


blank_node_in_output = True

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
                # if str(o) in obj_dicts.keys():
                if len([obj for obj in obj_dicts.keys() if obj in str(o)]) == 1:
                    if "/User/" in str(o) or "/Hashtag/" in str(o):  # modify into a list
                        obj_key = str(o).rsplit("/", 1)[0] + "/"
                        obj_name = str(o).rsplit("/", 1)[1]
                        node_output["p" + str(prop_counter)] = "They " + preds_dict[str(p)] + " " + obj_dicts[obj_key] + obj_name

                    else:
                        node_output["p" + str(prop_counter)] = preds_dict[str(p)] + \
                                                               " \"" + obj_dicts[str(o)].strip() + "\""

                    prop_counter += 1

                elif any(blank_node in str(o) for blank_node in blank_nodes):
                    node_output["p" + str(prop_counter)] = "They share the property \"" \
                                                           + preds_dict[str(p)] \
                                                               .replace(" is", "") \
                                                               .replace(":", "") \
                                                               .replace("They", "") \
                                                               .replace("Their", "") \
                                                               .strip() \
                                                           + " " \
                                                           + "\", all of them referencing the same resource " \
                                                             "not further described in the dataset"

                    relative_start[str(o)] = str(iteration + 1) + ":" + str(node_counter) + ":p" + str(prop_counter)
                    prop_counter += 1

                    """
                    elif "http" not in o and blank_node_in_output:
                        output += str(iteration + 1) + "." + str(prop_counter) + ") They all present the same property related to what " \
                                  + preds_dict[str(p)] + " in their description but with different values\n"

                        bnode_id[str(o)] = str(iteration + 1) + "." + str(prop_counter)
                    """

                elif "http" not in o and blank_node_in_output:
                    node_output["p" + str(prop_counter)] = "They share the property \"" \
                                                           + preds_dict[str(p)] \
                                                               .replace(" is", "") \
                                                               .replace(":", "") \
                                                               .replace("They", "") \
                                                               .replace("Their", "") \
                                                               .strip() \
                                                           + "\" each one of them referencing some resource"

                    #relative_start[str(o)] = [iteration + 1, node_counter, "p" + str(prop_counter)]
                    relative_start[str(o)] = str(iteration + 1) + ":" + str(node_counter) + ":p" + str(prop_counter)

                    prop_counter += 1

                neighbours.append(o)

                lvl_output[node_counter] = node_output

                if iteration > 0 and str(node) in relative_start.keys():
                    # relative_end[str(node)] = node_output
                    # relative_end[str(node)] = str(iteration + 1) + ":" + str(node_counter) + ":p" + str(prop_counter)
                    for preps in node_output.keys():
                        relative_end[str(iteration + 1) + ":" + str(node_counter) + ":" + preps] = str(node)

        # output += "\n\n"

    to_explore = [res for res in neighbours if str(res) not in explored]


    output[iteration+1] = lvl_output


'''
relative_union = {}
relative_union_index = {}
for item_s in relative_start.keys():
    for item_e in relative_end.keys():
        if item_s == item_e:
            relative_union[relative_start[item_s]] = relative_end[item_e]

relative_union["2:2:p1"] = {"p2": "lol", "p1": "lal"}
output[3] = {1: {"p1": "lol", "p2": "lal"}}
final_output = "The resources in analysis present the following properties in common: \n\n"

""" from depth 1 get root node """

lvl_1 = output[1][1]
prep_counter = 0

""" for lvl 2 only """
for prep in lvl_1.keys():
    prep_counter += 1
    final_output += str(prep_counter) + ") " + lvl_1[prep]
    rel_key = "1:1:" + prep
    if rel_key in relative_union.keys():
        final_output += " which "
        for rel_prep in relative_union[rel_key]:
            final_output += relative_union[rel_key][rel_prep].replace("They", "").replace(" are ", " is ") + " and "

        final_output = final_output[:-4]

    final_output += "\n"

'''


# def adjust_predicate(trad):
#    """ replacing third person plural with third person singular  """
#    trad.replace("They", "").replace(" are ", " is ")
#    return trad


def adjust_predicate(trad):
    """ replacing third person plural with third person singular  """
    t = trad.replace(" each one ", " ")\
        .replace(" some ", " a ")\
        .replace("They", "")\
        .replace(" are ", " is ")\
        .replace(" have ", " has ")\
        .replace("Their property", "has the property")\
        .replace("Their ", "its ")
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
