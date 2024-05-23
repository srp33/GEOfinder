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

# get collection
chroma_client = chromadb.PersistentClient(path=".")
my_collection = chroma_client.get_collection(name="embedding_collection")

# create representative encoding of sample ids
sample_ids = ["GSE0005", "GSE0008", "GSE0045", "GSE0031", "GSE0081", "GSE0099"]
sample_embeddings = []
for id in sample_ids:
    sample_embeddings.append(embedding_collection[id]["Embedding"])

avg_embedding = []
for i in range(len(sample_embeddings[0])):
    temp_sum = 0
    for embedding in sample_embeddings:
        temp_sum += float(embedding[i])
    avg_embedding.append(round(temp_sum/len(sample_embeddings), 5))

# query
similarity_results = my_collection.query(query_embeddings=avg_embedding, n_results=10)

print("OG docs:")
for id in sample_ids:
    print("\t" + embedding_collection[id]["Doc"])

print(f"\n\n similarity results: {similarity_results}")