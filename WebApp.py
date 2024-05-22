# Final Copy
import cherrypy
import re 
import json
import chromadb

class WebApp:

    @cherrypy.expose
    def index(self):
        #print(f"\n\n\n dictionary: \n\n\n {simpleDictionary}")
        return self.top_half_html()

    @cherrypy.expose
    def query(self, ids):
        return self.top_half_html(ids) + self.bottom_half_html(ids)

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

    def generate_error(bad_format_ids, not_found_ids, valid_ids):
        error_message = ""

        if bad_format_ids:
            error_message += f"<tr><td>Sorry, the following IDs you entered were formatted incorrectly: {', '.join(bad_format_ids)}</td></tr>"
        if not_found_ids:
            error_message +=f"<tr><td>The following IDs you entered were not found in our database: {', '.join(not_found_ids)}</td></tr>"
        if valid_ids:
            error_message +=f"<tr><td>The following IDs you entered were valid: {', '.join(valid_ids)}</td></tr>"
        
        return error_message
    
    def generate_query_results(input_ids):
        with open("collectionDict.json") as load_file:
            collection_dict = json.load(load_file)

        chroma_client = chromadb.PersistentClient(path="C:/Users/annat/OneDrive/Documents/College/Spring2024/PiccoloResearchLab/GEOfinder")
        my_collection = chroma_client.get_collection(name="collection1")
        
        similarityResults = my_collection.query(query_texts=[collection_dict[input_ids[i]] for i in range(len(input_ids))], n_results=5)

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
            return WebApp.generate_error(bad_format_ids, not_found_ids, valid_ids)
        else:
            return WebApp.generate_rows(valid_ids)
    
    


if __name__ == '__main__':
    cherrypy.quickstart(WebApp(), '/')


''' To-Do:
    - CSS: play around with Bulma more
    - look into how to import the python dictionary -  Convert Dct to dumps() (json pkg) - converts dct to str. Save json to file. 
        - webapp reads in json using loads() to convert to dct

    Later:
    - create vector database with. Access vec dbse after submit, display that info. Generate 100 vecs, size 100 (#s)

    Eventially:
    - file with data
'''
