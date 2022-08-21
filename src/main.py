# # %%
#
import rdflib
import random
import pandas as pd
from sklearn.cluster import KMeans

# from sklearn.decomposition import PCA
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import pyplot
# from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
# import networkx as nx
#
from knowledge_graph import *
from rdf2vec import RDF2VecTransformer

from lcs_rdf_graph import LCS

from rdf_graph_utils import rdf_to_plot

from copy import deepcopy

#
# # %%


def deblank(g):
    g1 = rdflib.Graph()
    for s, p, o in g:
        if "blank:r_" in s:
            s = rdflib.Literal(s.value.replace("blank", ""))
        if "blank:r_" in p:
            p = rdflib.Literal(p.value.replace("blank", ""))
        if "blank:r_" in o:
            o = rdflib.Literal(o.value.replace("blank", ""))

        g1.add((s, p, o))

    return g1


print(end='Loading data... ', flush=True)
g = rdflib.Graph()

g.parse('data/drugbank.nt', format="nt")
print('OK')
#
# # Extract all database drugs' URI
all_drugs_file = pd.read_csv('datasets/drugbank/all_drugs.tsv', sep='\t')
all_drugs = [rdflib.URIRef(x) for x in all_drugs_file['drug']]
#
# # Define irrelevant predicates
predicates = pd.read_csv('datasets/drugbank/bad_predicates.tsv', sep='\t')
predicates = [rdflib.URIRef(x) for x in predicates['predicate']]
#

stop_patterns = pd.read_csv('datasets/drugbank/stop_patterns.tsv', sep='\t')
stop_patterns = [x for x in stop_patterns['stopping_patterns']]

preds = pd.read_csv('datasets/drugbank/uninformative.tsv', sep='\t')
preds = [rdflib.URIRef(x) for x in preds['uninformative']]

# # %%
# # conversione da rdflib.Graph a KnowledgeGraph -> necessaria per applicare rdf2vec
# # con label_predicates si vanno ad indicare i predicati che verranno esclusi nella costruzione del kg risultante

kg = rdflib_to_kg(g, label_predicates=predicates)

# kg = rdflib_to_kg(g)
#
# # %%
# # estraggo un'istanza di knowledge graph per ogni drug presente in quello iniziale

i = 1
j = 1

kv = []
drugs = []
graphs = []

for drug in all_drugs:
    try:
        gi = extract_instance(kg, drug, 4)
        graphs.append(gi)
        drugs.append(drug)
        kv.append({'graph': gi, 'resource': drug})
        i += 1
    except Exception as e:
        j += 1

print('ok:' + str(i))
print('not imported: ' + str(j))

print(drugs)

#
#
#
# # Embeddings
transformer = RDF2VecTransformer(wl=False, max_path_depth=4000, vector_size=15, walks_per_graph=1)
# transformer = RDF2VecTransformer()
transformer.fit(graphs, drugs)
embeddings = transformer.transform(graphs, drugs)
# transformer.fit_transform(kg, all_drugs)
#

print("Embeddings created")

"""

import matplotlib.pyplot as plt

distortions = []
K = range(5, 100)
for k in K:
    kmeanModel_3 = KMeans(n_clusters=k)
    preds = kmeanModel_3.fit_predict(embeddings)
    distortions.append(kmeanModel_3.inertia_)
    centers = kmeanModel_3.cluster_centers_

    score = silhouette_score(embeddings, preds)
    print("For n_clusters = {}, silhouette score is {})".format(k, score))

plt.figure(figsize=(16, 8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()
"""

kmeans = KMeans(n_clusters=24)
km = kmeans.fit(embeddings)
y_kmeans = kmeans.predict(embeddings)

print("clustering models created")

# STAMPO PER OGNI RISORSA IL CLUSTER A CUI CORRISPONDE, IN MODO DA POTERNE PRELEVARE PER IL MOMENTO
# DUE APPARTENENTI ALLO STESSO CLUSTER

print("#### <cluster number> : <risorsa>")
k = 0
for y in y_kmeans:
    print(str(k) + ': ' + str(y))
    k += 1

"""

# SELEZIONO I GRAFI RELATIVI A DUE DRUGS RISULTANTI NELLO STESSO CLUSTER

r1 = 244
r2 = 3160

drug1 = drugs[r1]
drug2 = drugs[r2]

graph1 = graphs[r1]
graph2 = graphs[r2]

print(drug1)
print(drug2)


# CREAZIONE DEL GRAFO OTTENUTO DAL LCS
rdflib_x_Tx = LCS(graph1, graph2, depth=2, stop_patterns=stop_patterns, uninformative_triples=preds)
rdflib_x_Tx.find()

print(len(rdflib_x_Tx))
rdf_to_plot(rdflib_x_Tx)

rdflib_x_Tx = LCS(rdflib_x_Tx, graphs[5596], depth=2, stop_patterns=stop_patterns, uninformative_triples=preds)
rdflib_x_Tx.find()


print(rdflib_x_Tx)

# RAPPRESENTAZIONE GRAFICA IN PLOT DEL GRAFO
# rdf_to_plot(rdflib_x_Tx)


"""

clusters = {i: [] for i in range(kmeans.n_clusters)}
i = 0
for j in y_kmeans:
    clusters[j].append(i)
    i += 1

# cluster da analizzare
# k = 2
k = min(clusters.keys(), key=lambda a: len(clusters[a]))
L = len(clusters[k])

print("esploro il cluster: " + str(k) + " con dimensione " + str(L))

# risorsa iniziale
resource_1 = random.choice(clusters[k])
graph_1 = graphs[resource_1]

print("risorsa iniziale: " + str(resource_1) + "di dim -> " + str(len(kg_to_rdflib(graph_1, 2))))

clusters[k].remove(resource_1)
explored_resoures = [resource_1]

while clusters[k]:
    try:
        resource_2 = random.choice(clusters[k])
        print("LCS with resource: " + str(resource_2))
        clusters[k].remove(resource_2)

        # seed
        seed = LCS(graph_1, graphs[resource_2], depth=2, stop_patterns=stop_patterns, uninformative_triples=preds)
        seed.find()
        print("dim LCS tra " + str(explored_resoures) + " -> " + str(len(seed)))
        graph_1 = seed

        explored_resoures.append(resource_2)

        print("Trovato LCS tra: " + str(explored_resoures))

    except Exception as e:
        print("got exception: " + str(e))

rdf_to_plot(seed)
print("LCS finale tra le risorse: " + str(explored_resoures))
