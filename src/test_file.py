import os, sys
import datetime
"""
directory = "outputs/drugbank/oLast_NQ_NEW_optimized" + str(datetime.datetime.now()).replace(":", ".").replace(" ", "_")
if not os.path.exists(directory):
    os.mkdir(directory)
"""
iteration = 0
directory = "outputs/drugbank/oLast_NQ_NEW_optimized2022-10-30_16.47.12.228172"
fileopencount = open(directory + "/output_tmp_LCS_" + str(iteration) + ".nt", "r")
filecount = len(fileopencount.readlines())
print("Count: ", filecount)
