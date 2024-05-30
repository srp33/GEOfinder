# Final Copy
import cherrypy
import re 
import json
import chromadb
import traceback 
import pandas as pd
from sys import argv

class WebApp:

    @cherrypy.expose
    def index(self):
        #print(f"\n\n\n dictionary: \n\n\n {simpleDictionary}")
        # try:
        return self.top_half_html()
        # except:
        return self.render_error()

    # a) 1-10, b) 11-50, c) 51-100, d) 101-500, e) 501-1000, f) 1000+
    @cherrypy.expose
    def query(self, ids, human="", mouse="", rat="", a="", b="", c="", d="", e="", f="", rnaSeq="", microarr=""):
        metadata_dct = self.make_metadata_dct([human, mouse, rat], [a, b, c, d, e, f], [rnaSeq, microarr])
        # try:
        return self.top_half_html(ids) + self.bottom_half_html(ids, metadata_dct)
        # except:
        return self.render_error()

    #Internal:

    def make_metadata_dct(self, species, num_samples, platform):
        metadata_dct={}
        if species:
            metadata_dct["Species"] = [val for val in species if val]
        if num_samples:
            metadata_dct["Num Samples"] = [val for val in num_samples if val]
        if platform:
            metadata_dct["Platform"] = [val for val in platform if val]

        print(f"\n\n\n{metadata_dct}\n\n\n\n")
        return metadata_dct
    
    #use pandas to make a dataframe that meets user filter requirements, then returns a list of corresponding IDs
    def filter_ids_by_metas(metadata_dct):
        dataFrame = pd.read_csv("dummy_metadatas.tsv", index_col=0, sep="\t")
        for key, value_list in metadata_dct.items():
            dataFrame = dataFrame[dataFrame[key].isin(value_list)]
        return dataFrame.index.tolist()

    def create_id_list():
        print("\nIn create_id_lst()\\n")
        database_ids = []
        with open("csvFiles/testChromaIDs.csv") as id_file:
            for id in id_file.read().split(","):
                database_ids.append(id.strip().strip('"'))
        return database_ids

    def top_half_html(self, ids = ""):
        print("\n in top_half()\n")
        return f"""
        <html>
        <link 
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css"
        >
        <head></head>
        <body class="mx-6">
        <h1 class="mt-3 subtitle is-3 has-text-centered is-family-sans-serif"><u>Enter GEO Accession IDs:</u></h1>
        <form action="/query" method="post">
            <textarea
                class="content is-medium textarea has-fixed-size textarea is-hovered textarea is-info"
                name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)" rows="10"></textarea>

        <h1 class="mt-3 subtitle is-4 is-family-sans-serif"><u>Filters:</u></h1>
            <div class="columns">
                <div class="column is-2"><strong>Species:</strong><br>
                    <input type="checkbox" id="human" name="human" value="human">
                    <label for="vehicle1">Human</label><br></p>
                    <input type="checkbox" id="mouse" name="mouse" value="mouse">
                    <label for="mouse">Mouse</label><br>
                    <input type="checkbox" id="rat" name="rat" value="rat">
                    <label for="rat">Rat</label><br><br>
                </div>
                <div class="column is-2"><strong># Samples:</strong><br>
                    <input type="checkbox" id="a" name="a" value="1-10">
                    <label for="vehicle1">1-10</label><br></p>
                    <input type="checkbox" id="b" name="b" value="11-50">
                    <label for="mouse">11-50</label><br>
                    <input type="checkbox" id="c" name="c" value="51-100">
                    <label for="rat">51-100</label><br>
                    <input type="checkbox" id="d" name="d" value="101-500">
                    <label for="rat">101-500</label><br>
                    <input type="checkbox" id="501-1000" name="e" value="501-1000">
                    <label for="rat">501-1000</label><br>
                    <input type="checkbox" id="f" name="f" value="1000+">
                    <label for="rat">1000+</label><br><br>
                </div>
                <div class="column is-2"><strong>Platform:</strong><br>
                    <input type="checkbox" id="rnaSeq" name="rnaSeq" value="RNA sequencing">
                    <label for="rnaSeq">RNA Sequencing</label><br></p>
                    <input type="checkbox" id="microarr" name="microarr" value="Microarrays">
                    <label for="microarr">Microarrays</label><br><br><br><br><br><br>
                </div>
            </div>
        <button class="button is-info" type="submit">Submit</button>        
        </form>            
        """
    #class="mt-3 subtitle is-3 has-text-centered"
    #class="content is-large has-text-black"
    #<input type="text" name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)">
    #rows="20" cols="50
    
    #<input type="text" name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)">
    def bottom_half_html(self, ids, metadata_dct):
        print("\n in bottom_half()\n")
        return f"""
        <h1 class="py-4 mt-3 subtitle is-3 has-text-centered is-family-sans-serif">Relevant Studies:</h1>
        <div class="columns is-centered">
            <div class="columns is-three-quarters">
                <table class="table is-size-medium" id="myTable" border="1">
                    {self.handle_input_ids(ids, metadata_dct)}
                </table>
            </div>
        </div>
        </body>
        </html>
        """
    
    #user friendly error message with the try-except blocks
    def render_error(self):
        return f"""
        <html>
        <link 
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css"
        >
            <body>
                <h1 class="mt-3 subtitle is-3 has-text-centered is-family-sans-serif">An error occured. Please contact the administrator.</h1>
            </body>
        </html>
        """

    def invalid_id_msg(bad_format_ids, not_found_ids, valid_ids):
        error_message = ""
        if bad_format_ids:
            error_message += f"<tr><td>Sorry, the following IDs you entered were formatted incorrectly: {', '.join(bad_format_ids)}</td></tr>"
        if not_found_ids:
            error_message +=f"<tr><td>The following IDs you entered were not found in our database: {', '.join(not_found_ids)}</td></tr>"
        if valid_ids:
            error_message +=f"<tr><td>The following IDs you entered were valid: {', '.join(valid_ids)}</td></tr>"
        return error_message
    
    #returns a dictionary of the closest results to the user IDs input
    def generate_query_results(input_ids):
        with open("embeddingCollectionDict.json") as load_file:
            collection_dict = json.load(load_file)

        chroma_client = chromadb.PersistentClient(path=".")
        my_collection = chroma_client.get_collection(name="embedding_collection")
        
        print(f"\n\n\n\n input ids: {input_ids}")
        input_embeddings = [collection_dict[input_ids[i]]["Embedding"] for i in range(len(input_ids))]

        avg_embedding = []
        for i in range(len(input_embeddings[0])):
            temp_sum = 0
            for embedding in input_embeddings:
                temp_sum += embedding[i]
            avg_embedding.append(round(temp_sum/len(input_embeddings), 5))

        similarityResults = my_collection.query(query_embeddings=avg_embedding, n_results=5)
        
        #similarityResults = my_collection.query(query_texts=collection_dict[input_ids[0]]["Doc"], n_results=5)
        formatted_dict = {}
        for i in range(5):
            formatted_dict[similarityResults['ids'][0][i]] = {"Description": similarityResults['documents'][0][i]}
                                                            #    "Species": similarityResults['metadatas'][0][i]['Species'], \
                                                            #         "# Samples": similarityResults['metadatas'][0][i]['Num Samples'], \
                                                            #             "Platform": similarityResults['metadatas'][0][i]['Platform']}
        return formatted_dict
        #TO DO return list of IDS
    
    #calls generate_query_results and writes results in html code, to display results in a table 
    def generate_rows(valid_ids, metadata_dct={}):
        
        #TO DO loop through lists and return top 5 most similar, keep chromadb order 
        print(f"\n\n\nin generate rows, valid_ids: {valid_ids}")
        print(f"\n\n\nin generate rows, metadata_dict: {metadata_dct}")
        results_dict = WebApp.generate_query_results(valid_ids)
        filtered_ids = WebApp.filter_ids_by_metas(metadata_dct)

        for key, value in results_dict.items():
            if key in filtered_ids:
                print("found a match")
            else:
                print("no matches found between filtered dataFrame and query results")

        rows = "<tr> <th>GSE ID</th> <th>Description</th> <th>Species</th> <th># Samples</th> <th>Platform</th></tr>"
        for id in results_dict.keys():
            rows += f"<tr> <td>{id}</td> <td>{results_dict[id]['Description']}</td><td></tr>"
            #{results_dict[id]['Species']}</td> <td>{results_dict[id]['# Samples']}</td> <td>{results_dict[id]['Platform']}</td>   </tr>"
        return rows

    #checks for invalid input, if all input is valid then calls generate_rows 
    def handle_input_ids(self, ids, metadata_dct):
        print("\n in handle_input_ids()\n")
        if (ids == ""):
            return ""
        
        id_lst = re.split(r"\n|,",ids.strip())
        bad_format_ids = []
        not_found_ids = []
        valid_ids = []
        
        # access comprehensive list of ids from external csv
        database_ids = WebApp.create_id_list()

        for id in id_lst:
            id = id.strip().upper()

            if not re.search(r"GSE\d+",id):
                bad_format_ids.append(id)
            elif id not in database_ids:
                not_found_ids.append(id)
            else: 
                valid_ids.append(id)

        #test values: gse001, gse002, gse789, gse990, jkf292, fif404
        if bad_format_ids or not_found_ids:    
            return WebApp.invalid_id_msg(bad_format_ids, not_found_ids, valid_ids)
        else:
            print(f"\n\n\nin handle input, valid_ids: {valid_ids}")
            print(f"\n\n\nin handle input, metadata_dct: {metadata_dct}")
            return WebApp.generate_rows(valid_ids, metadata_dct)
    
    


if __name__ == '__main__':
    cherrypy.quickstart(WebApp(), '/')

'''
TO-DO
5/30
    - Use keyword functionality - if a user enters a phrase, identify the words that onehotencoding has seen before and query based on that 
    - jquery/javascript functionality without the form tag
    - in the render_error function, store the error message to a file so that the administrator can see what's going wrong
'''
