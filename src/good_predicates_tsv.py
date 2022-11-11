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
