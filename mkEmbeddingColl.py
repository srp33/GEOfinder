from sklearn.preprocessing import OneHotEncoder
import json
import re
import numpy as np
import chromadb

# Create synthesized "average" embedding. Representative of multiple inputs
with open("embeddingCollectionDict.json") as data_file:
    embedding_collection = json.load(data_file)

# convert all embedding values from strs to floats
for id in embedding_collection.keys():
    embedding_collection[id]["Embedding"] = [float(num) for num in embedding_collection[id]["Embedding"]]

#average_arr = np.average(X, axis=0)

chroma_client = chromadb.PersistentClient(path=".")
my_collection = chroma_client.create_collection(name="embedding_collection")

my_collection.add(ids = list(embedding_collection.keys()), \
                         documents=[inner_dct["Doc"] for inner_dct in list(embedding_collection.values())], \
                            embeddings=[inner_dct["Embedding"] for inner_dct in list(embedding_collection.values())])




# print(my_collection.query(query_embeddings=average_arr, n_results=5))

