import os, sys

directory = "outputs/drugbank/oLast_NQ_NEW_3"
if not os.path.exists(directory):
    os.mkdir(directory)

iteration = 0

fileopencount = open(directory + "/output_tmp_LCS_" + str(iteration) + ".nt", "r")
filecount = len(fileopencount.readlines())
print("Count: ", filecount)
