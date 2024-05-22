import json

def main():
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
        id_doc_dict[test_ids[i]] = test_docs[i]

    # Dump to json file
    with open("collectionDict.json", "w") as write_file:
        json.dump(id_doc_dict, write_file)


"""
To load json into dict:

    with open("collectionDict.json") as load_file:
        id_doc_dict = json.load(load_file)

"""

if __name__ == '__main__':
    main()