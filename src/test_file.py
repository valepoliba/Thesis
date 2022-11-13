"""
import os, sys
import datetime

directory = "outputs/drugbank/oLast_NQ_NEW_optimized" + str(datetime.datetime.now()).replace(":", ".").replace(" ", "_")
if not os.path.exists(directory):
    os.mkdir(directory)

iteration = 0
directory = "outputs/drugbank/oLast_NQ_NEW_optimized2022-10-30_16.47.12.228172"
fileopencount = open(directory + "/output_tmp_LCS_" + str(iteration) + ".nt", "r")
filecount = len(fileopencount.readlines())
print("Count: ", filecount)

array1 = [0,1]
array2 = []

print("array1: ", array1)
print("array2: ", array2)

array2 = array1

print("array1: ", array1)
print("array2: ", array2)

array1.append(2)

print("array1: ", array1)
print("array2: ", array2)

"""
"""
iteration = 0
filecount = 5

if iteration > 0 or (iteration == 0 and filecount > 1):
    print("Entro")
else:
    print("Non entro")


# Creo file good_predicates.tsv
import pandas as pd
import csv

allpredicates = pd.read_csv('datasets/drugbank/all_predicates.tsv', sep='\t')
badpredicates = pd.read_csv('datasets/drugbank/bad_predicates.tsv', sep='\t')
print("Count allpredicates: ", allpredicates.count())
print("Count badpredicates: ", badpredicates.count())
#print(badpredicates)

df = pd.concat([allpredicates, badpredicates]).drop_duplicates(keep=False)
#print(df)
print("Count: ", df.count())
df.to_csv('datasets/drugbank/good_predicates.tsv', index=False, quoting=csv.QUOTE_ALL)
"""

import rdflib
import pandas as pd
from rdflib import Graph, RDF
from rdflib.term import _is_valid_uri
from knowledge_graph import *
import shlex
"""
g = Graph()
g.parse('outputs/drugbank/oLast_NQ_NEW_3/output_tmp_LCS_0.nt')

good_predicates = pd.read_csv('datasets/drugbank/good_predicates.tsv', sep='\t')
good_predicates = [rdflib.URIRef(x) for x in good_predicates['good_predicates']]

path = 'outputs/drugbank/oLast_NQ_NEW_3/output_tmp_LCS_0.nt'

for s, p, o in g:
    if p in good_predicates:
        if _is_valid_uri(p):
            print(p)
"""

with open('datasets/drugbank/good_predicates.tsv', 'r') as good_predicates:
    gp = good_predicates.read().split()
outputnt = open('outputs/drugbank/oLast_NQ_NEW_3/output_tmp_LCS_0.nt', 'r')
outputietration =  open('outputs/drugbank/oLast_NQ_NEW_3/output_tmp_LCS_0_po_significant.nt', 'a')
filecount = 0
for line in outputnt.readlines():
        line = line.replace('<', '').replace('>', '')
        s, p, o, _ = shlex.split(line)
        if not ('_:blank_' in o) and not ('_:blank_' in p):
            for goodline in gp:
                if goodline == p:
                    outputietration.write(p + '\n')
                    filecount += 1

print("Count row: ", filecount)

#outputietration.close()
outputnt.close()
good_predicates.close()    

