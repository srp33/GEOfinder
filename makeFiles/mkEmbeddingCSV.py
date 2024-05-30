from sklearn.preprocessing import OneHotEncoder
import json
import re
import numpy as np
import chromadb
import csv 

#creates embedding from ID and document 

with open("collectionDict.json") as load_file:
            collection_dict = json.load(load_file)
    
input_docs = list(collection_dict.values())
# print(input_docs)
max_words = 0

for i in range(len(input_docs)):
    input_docs[i] = re.split( r" ", re.sub(r"[\.,]", r"", input_docs[i]))
    if len(input_docs[i]) > max_words:
            max_words = len(input_docs[i])

for i in range(len(input_docs)):
    while len(input_docs[i]) < max_words:
           input_docs[i].append("the")

# Create an instance of OneHotEncoder
encoder = OneHotEncoder(sparse_output=False)

# Learn the vocabulary and transform the data
embedding_list = encoder.fit_transform(input_docs).tolist()

with open("testChromaEmbeddings.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(embedding_list)