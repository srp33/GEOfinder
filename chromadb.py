import chromadb
import json

id_doc_dict = {}

# create comprehensive list of database ids and docs with imported json files
def get_id_doc_dict():
    print("\n in get_id_doc_dct()\n")
    global id_doc_dict 

    with open("collectionDict.json") as load_file:
       id_doc_dict = json.load(load_file)

def generate_collection():
    print("\n in generate_collection()\n")
    get_id_doc_dict()
    # create collection and populate with text data
    chroma_client = chromadb.Client()
    collection1 = chroma_client.create_collection(name="collection1")

    collection1.add(documents=list(id_doc_dict.values()), ids = list(id_doc_dict.keys()))
    return collection1

def dump_results(results):
    json_dict = json.dumps(results)
    with open("resultsDict.json", "w") as writeFile:
        writeFile.write(json_dict)

#right now, only has functionality for 1 ID !!!! ***come back and update         
def generate_results(input_ids):
    print("\n\nin generate_results()\n\n")

    my_collection = generate_collection()
    similarityResults = my_collection.query(query_texts=[id_doc_dict[input_ids[i]] for i in range(len(input_ids))], n_results=5)

    formatted_dict = {}
    for i in range(5):
        formatted_dict[similarityResults['ids'][0][i]] = {"Description": similarityResults['documents'][0][i], "Platform": "None", "Samples": "None"}

    # dump formatted results to json
    dump_results(formatted_dict)



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
