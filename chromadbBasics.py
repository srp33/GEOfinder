import chromadb
import json

def main():
    # create collection and populate with text data
    chroma_client = chromadb.Client()
    collection1 = chroma_client.create_collection(name="collection1")

    with open("testChromaDocuments.csv") as doc_file:
        test_docs = []
        for line in doc_file:
            test_docs.append(line.strip().strip(","))
            # print(line)

    with open("testChromaIDs.csv") as id_file:
        test_ids = id_file.read().split(",")

    
    collection1.add(
        documents=test_docs, 
        ids = test_ids
        )

    # test collection docs' similarity to query doc. print results
    similarityResults = collection1.query(query_texts=["The squirrel gathers nuts in the forest, scampering among the trees with agile grace."], n_results=5)
    print(type(similarityResults))
    print(similarityResults)

    # weird quotes.....********************
    filtered_dict = {}
    for i in range(5):
        
        filtered_dict[similarityResults['ids'][0][i]] = {"Description": similarityResults['documents'][0][i], "Platform": "None", "Samples": "None"}
    print(f"\n\n\n{filtered_dict}")

    # dump to json
    json_dict = json.dumps(filtered_dict)
    with open("myDict.json", "w") as writeFile:
        writeFile.write(json_dict)


if __name__ == "__main__":
    main()

''' Test docs:
    "The squirrel gathers nuts in the forest, scampering among the trees with agile grace.","The koala sleeps in the eucalyptus tree, cuddled up in a cozy ball, dreaming of leafy delights.","The otter slides down the riverbank, sleek and swift, a playful dance on the water's edge."

'''

'''Collection Examples:

(    
    documents=["The red fox jumps over the fence", "The brown chicken crosses the road", "The orange tiger swims across the river"],
    ids = ["GSE0001", "GSE0002", "GSE0003"]
)

'''
