import chromadb
import json

id_doc_dict = {}

# create comprehensive list of database ids and docs with imported json files

def create_id_doc_dict():
    print("\n in create_id_doc_dict()\n")
    with open("testChromaIDs.csv") as id_file:
        test_ids = []
        for id in id_file.read().split(","):
            test_ids.append(id.strip().strip('"'))

    with open("testChromaDocuments.csv") as doc_file:
        test_docs = []
        for line in doc_file:
            test_docs.append(line.strip().strip(",").strip('"'))

    for i in range(100):
        id_doc_dict[test_ids[i]] = test_docs[i]

#right now, only has functionality for 1 ID !!!! ***come back and update         
def generate_results(input_ids):
    print("\n\nin generate_results()\n\n")
    my_collection = generate_collection()
    similarityResults = my_collection.query(query_texts=[id_doc_dict[input_ids[i]] for i in range(len(input_ids))], n_results=5)
    # similarityResults = my_collection.query(query_texts=id_doc_dict[input_ids[0]], n_results=5)
    # print(type(similarityResults))
    # print(similarityResults)

    filtered_dict = {}
    for i in range(5):
        
        filtered_dict[similarityResults['ids'][0][i]] = {"Description": similarityResults['documents'][0][i], "Platform": "None", "Samples": "None"}
    # print(f"\n\n\n{filtered_dict}")

    # dump to json
    json_dict = json.dumps(filtered_dict)
    with open("myDict.json", "w") as writeFile:
        writeFile.write(json_dict)

def generate_collection():
    print("\n in generate_collection()\n")
    create_id_doc_dict()
    # create collection and populate with text data
    chroma_client = chromadb.Client()
    collection1 = chroma_client.create_collection(name="collection1")

    collection1.add(documents=list(id_doc_dict.values()), ids = list(id_doc_dict.keys()))
    return collection1


if __name__ == "__main__":
    pass

''' Test docs:
    "The squirrel gathers nuts in the forest, scampering among the trees with agile grace.","The koala sleeps in the eucalyptus tree, cuddled up in a cozy ball, dreaming of leafy delights.","The otter slides down the riverbank, sleek and swift, a playful dance on the water's edge."

'''

'''Collection Examples:

(    
    documents=["The red fox jumps over the fence", "The brown chicken crosses the road", "The orange tiger swims across the river"],
    ids = ["GSE0001", "GSE0002", "GSE0003"]
)

'''
