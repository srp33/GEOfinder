import chromadb

def main():
    # create collection and populate with text data
    chroma_client = chromadb.Client()
    collection1 = chroma_client.create_collection(name="collection1")
    collection1.add(
        documents=["The red fox jumps over the fence", "The brown chicken crosses the road", "The orange tiger swims across the river"],
        ids = ["id1", "id2", "id3"]
        )

    # test collection docs' similarity to query doc. print results
    similarityResults = collection1.query(query_texts=["The pink flamingo flies over the sea"], n_results=2)
    print(type(similarityResults))
    print(similarityResults)


if __name__ == "__main__":
    main()
