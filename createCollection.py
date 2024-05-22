import chromadb
import json

if __name__ == "__main__":
    with open("collectionDict.json") as load_file:
       id_doc_dict = json.load(load_file)

    # create collection and populate with data
    chroma_client = chromadb.PersistentClient(path="C:/Users/annat/OneDrive/Documents/College/Spring2024/PiccoloResearchLab/GEOfinder")
    collection1 = chroma_client.create_collection(name="collection1")

    collection1.add(documents=list(id_doc_dict.values()), ids = list(id_doc_dict.keys()))


'''
- Xseparate webpp and analData
- Xdont store results in json. direct access
- find way to anal multi vecors
- sort based on vector. (one hot encoding if need to average vectors to one)
'''

''' Test docs:
    "The squirrel gathers nuts in the forest, scampering among the trees with agile grace.","The koala sleeps in the eucalyptus tree, cuddled up in a cozy ball, dreaming of leafy delights.","The otter slides down the riverbank, sleek and swift, a playful dance on the water's edge."

'''

'''Collection Examples:

(   
    documents=["The red fox jumps over the fence", "The brown chicken crosses the road", "The orange tiger swims across the river"],
    ids = ["GSE0001", "GSE0002", "GSE0003"]
)

'''
