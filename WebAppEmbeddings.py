# Final Copy
import cherrypy
import re 
import json
import chromadb
import traceback 

class WebApp:

    @cherrypy.expose
    def index(self):
        #print(f"\n\n\n dictionary: \n\n\n {simpleDictionary}")
        try:
            return self.top_half_html()
        except:
            return self.render_error()


    @cherrypy.expose
    def query(self, ids):
        try:
            return self.top_half_html(ids) + self.bottom_half_html(ids)
        except:
            return self.render_error()

    #Internal:

    def create_id_list():
        print("\nIn create_id_lst()\\n")
        database_ids = []

        with open("testChromaIDs.csv") as id_file:
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
        <body>
        <h1 class="mt-3 subtitle is-3 has-text-centered is-family-sans-serif">Enter GEO Accession IDs:</h1>
        <form action="/query" method="post">
            <textarea
                class="content is-medium textarea has-fixed-size textarea is-hovered textarea is-info"
                name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)" rows="10"></textarea>
            <button class="button is-info" type="submit">Submit</button>
        </form>
        <script>
        function check_input() {{
                var input = document.getElementById('user_input').value;
                var button = document.getElementById('submit_button');
                button.disabled = input === '';
        }} 
        function submit_form() {{
            // Disable the submit button
            var button = document.getElementById('submit_button');
            var textarea = document.getElementById('user_input');
            button.disabled = true;
            textarea.value = "";
            textarea.placeholder = "loading results..."
            // call other function that's supposed to be called 
        }}
        </script>
            
        """
    #class="mt-3 subtitle is-3 has-text-centered"
    #class="content is-large has-text-black"
    #<input type="text" name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)">
    #rows="20" cols="50
    
    #<input type="text" name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)">
    def bottom_half_html(self, ids):
        print("\n in bottom_half()\n")
        return f"""
        <h1 class="py-4 mt-3 subtitle is-3 has-text-centered is-family-sans-serif">Relevant Studies:</h1>
        <div class="columns is-centered">
            <div class="columns is-three-quarters">
                <table class="table is-size-medium" id="myTable" border="1">
                    {self.generate_output_from_ids(ids)}
                </table>
            </div>
        </div>
        </body>
        </html>
        """
    
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
    
    def generate_query_results(input_ids):
        with open("embeddingCollectionDict.json") as load_file:
            collection_dict = json.load(load_file)

        chroma_client = chromadb.PersistentClient(path=".")
        my_collection = chroma_client.get_collection(name="embedding_collection")
        
        input_embeddings = [collection_dict[input_ids[i]]["Embedding"] for i in range(len(input_ids))]

        avg_embedding = []
        for i in range(len(input_embeddings[0])):
            temp_sum = 0
            for embedding in input_embeddings:
                temp_sum += embedding[i]
            avg_embedding.append(round(temp_sum/len(input_embeddings), 5))

        similarityResults = my_collection.query(query_embeddings=avg_embedding, n_results=5)

        formatted_dict = {}
        for i in range(5):
            formatted_dict[similarityResults['ids'][0][i]] = {"Description": similarityResults['documents'][0][i], "Platform": "None", "Samples": "None"}

        return formatted_dict
    
    def generate_rows(valid_ids):
        # Old code:
        # call analyzeData to create json file of answers
            # analyzeData.generate_results(valid_ids)

        results_dict = WebApp.generate_query_results(valid_ids)

        rows = "<tr> <th>GSE ID</th> <th>Description</th> <th>Platform</th> <th>Samples</th> </tr>"
        for id in results_dict.keys():
            rows += f"<tr> <td>{id}</td>  <td>{results_dict[id]['Description']}</td>  <td>{results_dict[id]['Platform']}</td>  <td>{results_dict[id]['Samples']}</td> </tr>"
        return rows

    def generate_output_from_ids(self, ids):
        print("\n in generate_table_rows()\n")
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
            return WebApp.generate_rows(valid_ids)
    
    


if __name__ == '__main__':
    cherrypy.quickstart(WebApp(), '/')


''' To-Do: 5/23
    - try except block around every function in WebApp
    - Create file with dummy metadatas for each dataset: spec name (hu, mouse, rat), num samples (int 1-10, 11-50, 51-100, 101-500, 501-1000, 1000+), platform (RNA seq, Microarray)
        - add way to filter based on these on WebApp
    - Pandas

    - Long term: enter text, vs GSE id, with keywords to base search on

'''