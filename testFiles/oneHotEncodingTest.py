from sklearn.preprocessing import OneHotEncoder
import json
import re
import numpy as np
import chromadb
import csv 
             

##########
# Create database json file with {id: [doc, embedding]}
##########
'''
id_doc_dict = {}

# Create dictionary from lists
with open("testChromaIDs.csv") as id_file:
    test_ids = []
    for id in id_file.read().split(","):
        test_ids.append(id.strip().strip('"'))

with open("testChromaDocuments.csv") as doc_file:
    test_docs = []
    for line in doc_file:
        test_docs.append(line.strip().strip(",").strip('"'))

for i in range(100):
    id_doc_dict[test_ids[i]] = [test_docs[i], X[i]]

# Dump to json file
with open("encodingCollectionDict.json", "w") as write_file:
    json.dump(id_doc_dict, write_file)
    '''