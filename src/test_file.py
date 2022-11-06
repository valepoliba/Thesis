import os, sys
import datetime
"""
directory = "outputs/drugbank/oLast_NQ_NEW_optimized" + str(datetime.datetime.now()).replace(":", ".").replace(" ", "_")
if not os.path.exists(directory):
    os.mkdir(directory)

iteration = 0
directory = "outputs/drugbank/oLast_NQ_NEW_optimized2022-10-30_16.47.12.228172"
fileopencount = open(directory + "/output_tmp_LCS_" + str(iteration) + ".nt", "r")
filecount = len(fileopencount.readlines())
print("Count: ", filecount)
"""
"""
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
iteration = 0
filecount = 5

if iteration > 0 or (iteration == 0 and filecount > 1):
    print("Entro")
else:
    print("Non entro")