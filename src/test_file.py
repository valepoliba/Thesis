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
"""
import rdflib
import pandas as pd
from rdflib import Graph, RDF
from rdflib.term import _is_valid_uri
from knowledge_graph import *
import shlex

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
                    outputietration.write(s + ' ' + p + ' ' + o + ' ' + _ + ' ' + '\n')
                    filecount += 1

print("Count row: ", filecount)

outputietration.close()
outputnt.close()
good_predicates.close()    
"""
#po1 = pd.read_csv('outputs/drugbank/po_significant/oLast_NQ_NEW_2022-11-16_15.11.01.877589/output_tmp_LCS_0_po_significant.nt', sep='\t')
#po2 = pd.read_csv('outputs/drugbank/po_significant/oLast_NQ_NEW_2022-11-16_15.11.01.877589/output_tmp_LCS_1_po_significant.nt', sep='\t')
#print("Count po1: ", po1.count())
#print("Count po2: ", po2.count())
#df = pd.concat([po1, po2])
#print(df)
#print("Count: ", df.count())
"""
po1 = open('outputs/drugbank/po_significant/oLast_NQ_NEW_2022-11-16_15.11.01.877589/output_tmp_LCS_0_po_significant.nt', 'r')
po2 = open('outputs/drugbank/po_significant/oLast_NQ_NEW_2022-11-16_15.11.01.877589/output_tmp_LCS_1_po_significant.nt', 'r')
outputietrationdifference =  open('outputs/drugbank/po_significant/oLast_NQ_NEW_2022-11-16_15.11.01.877589/output_tmp_LCS_0_po_difference.nt', 'a')
for line in po1.readlines():
        line = line.replace('<', '').replace('>', '')
        s, p, o, _ = shlex.split(line)
        po2.seek(0)
        for line2 in po2.readlines():
            line2 = line2.replace('<', '').replace('>', '')
            s2, p2, o2, dot = shlex.split(line2)
            if p != p2 or o != o2:
                outputietrationdifference.write('DIFFERENCE' + '\n')
                outputietrationdifference.write(s + ' ' + p + ' ' + o + ' ' + _ + ' ' + '\n')
                outputietrationdifference.write(s2 + ' ' + p2 + ' ' + o2 + ' ' + dot + ' ' + '\n\n')

outputietrationdifference.close()
"""
"""
if iteration != 0:
    po1 = open(directory + '/output_tmp_LCS_' + str(iteration-1) + '_po_significant.nt', 'r')
    po2 = open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_significant.nt', 'r')
    outputietrationdifference =  open(directory + '/output_tmp_LCS_' + str(iteration) + '_po_difference.nt', 'a')
    for line in po1.readlines():
            line = line.replace('<', '').replace('>', '')
            s, p, o, _ = shlex.split(line)
            po2.seek(0)
            for line2 in po2.readlines():
                line2 = line2.replace('<', '').replace('>', '')
                s2, p2, o2, dot = shlex.split(line2)
                if p != p2 or o != o2:
                    outputietrationdifference.write('DIFFERENCE' + '\n')
                    outputietrationdifference.write(s + ' ' + p + ' ' + o + ' ' + _ + ' ' + '\n')
                    outputietrationdifference.write(s2 + ' ' + p2 + ' ' + o2 + ' ' + dot + ' ' + '\n\n')

    outputietrationdifference.close()
"""  
"""
outputnt = open('outputs\drugbank\po_significant\oLast_NQ_NEW_2022-11-16_16.01.44.440238\output_tmp_LCS_0.nt', 'r')
for line in outputnt.readlines():
    line = line.replace('<', '').replace('>', '')
    s, p, o, _ = shlex.split(line)
    if not ('_:blank_' in p) and not ('_:blank_' in o) and ('http' in o):
        print(s + ' ' + p + ' ' + o + ' ' + _ + ' ' + '\n')

import difflib
import os
 
with open('outputs\drugbank\po_significant\oLast_NQ_NEW_2022-11-17_16.27.09.816007\output_tmp_LCS_0_po_significant.nt') as file_1:
    file_1_text = file_1.readlines()
 
with open('outputs\drugbank\po_significant\oLast_NQ_NEW_2022-11-17_16.27.09.816007\output_tmp_LCS_1_po_significant.nt') as file_2:
    file_2_text = file_2.readlines()
outputietrationdifference =  open('outputs\drugbank\po_significant\oLast_NQ_NEW_2022-11-17_16.27.09.816007\output_tmp_LCS_' + str(iteration) + '_po_difference.nt', 'a')
outputietrationdifference =  open('test1.nt', 'a')
# Find and print the diff:
for line in difflib.unified_diff(
        file_1_text, file_2_text, fromfile=str(file_1), tofile=str(file_2), lineterm='', n=0):
    #print(line)
    outputietrationdifference.write(line + '\n')

outputietrationdifference.close()
os.remove('test1.nt')
"""

"""
valueTo1={"a","b","c"}

if valueTo1.has_key("a"):
        print "Found key in dictionary"

import shlex

outputnt = open('outputs\drugbank\po_significant\oLast_NQ_NEW_2022-11-21_18.01.19.886840\output_tmp_LCS_0.nt', 'r')
outputietration =  open('outputs\drugbank\po_significant\oLast_NQ_NEW_2022-11-21_18.01.19.886840\output_tmp_LCS_0_different_predicates.nt', 'a')
temparray = []
filecount = 0   
for line in outputnt.readlines():
        line = line.replace('<', '').replace('>', '')
        s, p, o, _ = shlex.split(line)
        if not (p in temparray):
            temparray.append(p)
            
print('Different predicates count: ' + str(len(temparray)))
outputietration.write(str('\n'.join(temparray)) + '\n')
outputietration.write('\n' + '#######' + '\n' + 'Different predicates count: ' + str(len(temparray)))
"""

from rdf_graph_utils import diff_pred_significant
directory = 'outputs/drugbank/po_significant/oLast_NQ_NEW_2022-11-21_18.01.19.886840'
iteration = 0

diff_pred_significant(directory, iteration)

