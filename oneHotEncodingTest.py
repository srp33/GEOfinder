from sklearn.preprocessing import OneHotEncoder
import json
import re
import numpy as np
import chromadb

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
X = encoder.fit_transform(input_docs).tolist()



# Create synthesized "average" encoding. Representative of multiple inputs
# average_arr = np.average(X, axis=0)

# chroma_client = chromadb.PersistentClient(path="C:/Users/annat/OneDrive/Documents/College/Spring2024/PiccoloResearchLab/GEOfinder")
# my_collection = chroma_client.get_collection(name="collection1")
        
# print(my_collection.query(query_embeddings=average_arr, n_results=5))

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