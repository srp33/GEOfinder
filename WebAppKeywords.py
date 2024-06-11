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
        try:
            return self.top_half_html()
        except:
            with open("error.txt", "w") as error_file:
                traceback.print_exc(file=error_file)
            return self.render_error()

    # a) 1-10, b) 11-50, c) 51-100, d) 101-500, e) 501-1000, f) 1000+
    @cherrypy.expose
    def query(self, ids, human="", mouse="", rat="", a="", b="", c="", d="", e="", f="", rnaSeq="", microarr="", searchType="geoID"):
        print("\nReceived input:", ids, human, mouse, rat, a, b, c, d, e, f, rnaSeq, microarr)
        print(f"searchType: {searchType}, type: {type(searchType)}")

        metadata_dct = self.make_metadata_dct([human, mouse, rat], [a, b, c, d, e, f], [rnaSeq, microarr])
        print(f"\n\n\nIn query, metadata_dct:{metadata_dct}\n\n\n\n")

        try:
            return self.bottom_half_html(ids, metadata_dct, searchType)
        except:
            with open("error.txt", "w") as error_file:
                traceback.print_exc(file=error_file)
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

        return metadata_dct
    
    #use pandas to make a dataframe that meets user filter requirements, then returns a list of corresponding IDs
    def filter_ids_by_metas(metadata_dct):
        dataFrame = pd.read_csv("dummy_metadatas.tsv", index_col=0, sep="\t")
        for key, value_list in metadata_dct.items():
            if(value_list):
                dataFrame = dataFrame[dataFrame[key].isin(value_list)]
        return dataFrame.index.tolist()

    def create_id_list():
        database_ids = []
        with open("csvFiles/testChromaIDs.csv") as id_file:
            for id in id_file.read().split(","):
                database_ids.append(id.strip().strip('"'))
        return database_ids

    def top_half_html(self, ids = ""):
        return """
            <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GSE Search</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<style>
.grayed-out {
    color: #888888; /* Gray color */
}
</style>
</head>
<body>
<h1 class="mt-3 subtitle is-3 has-text-centered is-family-sans-serif"><u>Enter GEO Accession IDs or Keywords:</u></h1>

<h1 class="mt-3 subtitle is-4 is-family-sans-serif"><u>Search by:</u></h1>
<input type="radio" id="geoID" name="searchBy" value="geoID">
<label for="geoID">GEO IDs</label>
<input type="radio" id="keyword" name="searchBy" value="keyword">
<label for="keyword">Keywords</label><br><br>

<textarea id="inputText" class="content is-medium textarea has-fixed-size textarea is-hovered textarea is-info" placeholder="Enter IDs (ie. GSE123, GSE456)" rows="10"></textarea>

<h1 class="mt-3 subtitle is-4 is-family-sans-serif"><u>Filters:</u></h1>
<div class="columns">
    <div class="column is-2"><strong>Species:</strong><br>
        <input type="checkbox" id="human" name="human" value="human">
        <label for="human">Human</label><br>
        <input type="checkbox" id="mouse" name="mouse" value="mouse">
        <label for="mouse">Mouse</label><br>
        <input type="checkbox" id="rat" name="rat" value="rat">
        <label for="rat">Rat</label><br>
    </div>
    <div class="column is-2"><strong># Samples:</strong><br>
        <input type="checkbox" id="a" name="a" value="1-10">
        <label for="a">1-10</label><br>
        <input type="checkbox" id="b" name="b" value="11-50">
        <label for="b">11-50</label><br>
        <input type="checkbox" id="c" name="c" value="51-100">
        <label for="c">51-100</label><br>
        <input type="checkbox" id="d" name="d" value="101-500">
        <label for="d">101-500</label><br>
        <input type="checkbox" id="e" name="e" value="501-1000">
        <label for="e">501-1000</label><br>
        <input type="checkbox" id="f" name="f" value="1000+">
        <label for="f">1000+</label><br>
    </div>
    <div class="column is-2"><strong>Platform:</strong><br>
        <input type="checkbox" id="rnaSeq" name="rnaSeq" value="RNA sequencing">
        <label for="rnaSeq">RNA Sequencing</label><br>
        <input type="checkbox" id="microarr" name="microarr" value="Microarray">
        <label for="microarr">Microarray</label><br><br><br><br><br>
    </div>
</div>

<button id="submitButton" class="button is-info" disabled>Submit</button>

<script>
$(document).ready(function() {
    var searchType = 'geoID';

    $('#inputText').keyup(function() {
        var inputText = $(this).val();
        if (inputText.length > 0) {
            $('#submitButton').prop('disabled', false);
            $(this).removeClass('grayed-out'); // Remove grayed-out class to turn text black
        } else {
            $('#submitButton').prop('disabled', true);
        }
    });

    $('input[type=radio][name=searchBy]').change(function() {
        searchType = $(this).val(); 
    });

    $('#submitButton').click(function() {
        var inputText = $('#inputText').val();
        var checkboxValues = {};
        
        $('input[type=checkbox]').each(function() {
            checkboxValues[$(this).attr('name')] = $(this).is(':checked') ? $(this).val() : '';
        });

        $(this).prop('disabled', true); // Disable the button
        $('#inputText').addClass('grayed-out'); // Add gray color and disable textarea

        $.ajax({
            type: 'POST',
            url: '/query',
            data: {
                ids: inputText,
                human: checkboxValues['human'],
                mouse: checkboxValues['mouse'],
                rat: checkboxValues['rat'],
                a: checkboxValues['a'],
                b: checkboxValues['b'],
                c: checkboxValues['c'],
                d: checkboxValues['d'],
                e: checkboxValues['e'],
                f: checkboxValues['f'],
                rnaSeq: checkboxValues['rnaSeq'],
                microarr: checkboxValues['microarr'],
                searchType: searchType
            },
            success: function(response) {
                // Handle success response
                console.log(response);
                $('#content').html(response);
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error(xhr.responseText);
            }
        });
    });
});
</script>

<div id="content"></div>

</body>
</html>
        """
    
    def bottom_half_html(self, ids, metadata_dct, searchType):
        print("\n in bottom_half()\n")
        return f"""
        
        <div class="columns is-centered">
            <div class="columns is-three-quarters">
                <table class="table is-size-medium" id="myTable" border="1">
                    {self.handle_input_ids(ids, metadata_dct, searchType)}
                </table>
            </div>
        </div>
        <script>
        $('#submitButton').prop('disabled', false);
        </script>
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
        
        input_embeddings = [collection_dict[input_ids[i]]["Embedding"] for i in range(len(input_ids))]

        avg_embedding = []
        for i in range(len(input_embeddings[0])):
            temp_sum = 0
            for embedding in input_embeddings:
                temp_sum += embedding[i]
            avg_embedding.append(round(temp_sum/len(input_embeddings), 5))

        num_results = 50
        similarityResults = my_collection.query(query_embeddings=avg_embedding, n_results=num_results)

        #similarityResults = my_collection.query(query_texts=collection_dict[input_ids[0]]["Doc"], n_results=5)
        formatted_dict = {}
        for i in range(num_results):
            formatted_dict[similarityResults['ids'][0][i]] = {"Description": similarityResults['documents'][0][i]}
                                                            #    "Species": similarityResults['metadatas'][0][i]['Species'], \
                                                            #         "# Samples": similarityResults['metadatas'][0][i]['Num Samples'], \
                                                            #             "Platform": similarityResults['metadatas'][0][i]['Platform']}
        return list(formatted_dict.keys())
    
    #calls generate_query_results and writes results in html code, to display results in a table 
    def generate_rows(valid_ids, metadata_dct={}):
 
        results_ids = WebApp.generate_query_results(valid_ids)
        filtered_ids = WebApp.filter_ids_by_metas(metadata_dct)
        match_ids = []

        for id in results_ids:
            if not (id in valid_ids) and (id in filtered_ids):
                match_ids.append(id)

        dataFrame = pd.read_csv("dummy_metadatas.tsv", index_col=0, sep="\t")
        dataFrame = dataFrame.loc[match_ids]
            
        if not match_ids:
            return "<h1>Sorry, there are no results that match your filter choices.</h1>"

        rows = "<tr> <th>GSE ID</th> <th>Description</th> <th>Species</th> <th># Samples</th> <th>Platform</th></tr>"
        for id in match_ids:
            rows += f'<tr> <td>{id}</td> <td>{dataFrame.loc[id,"Description"]}</td> \
                <td>{dataFrame.loc[id,"Species"]}</td> <td>{dataFrame.loc[id,"Num Samples"]}</td> \
                    <td>{dataFrame.loc[id,"Platform"]}</td> </tr>'
            #{results_dict[id]['Species']}</td> <td>{results_dict[id]['# Samples']}</td> <td>{results_dict[id]['Platform']}</td>   </tr>"
        return rows

    #checks for invalid input, if all input is valid then calls generate_rows 
    def handle_input_ids(self, ids, metadata_dct, searchType):
        
        if (ids == ""):
            return ""
        elif searchType=="geoID":  
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
            return '<caption class="py-4 mt-3 subtitle is-3 has-text-centered is-family-sans-serif">ERROR:</caption>' + \
                WebApp.invalid_id_msg(bad_format_ids, not_found_ids, valid_ids)
        else:
            return '<caption class="py-4 mt-3 subtitle is-3 has-text-centered is-family-sans-serif">Relevant Studies:</caption>' + \
                WebApp.generate_rows(valid_ids, metadata_dct)
    
    


if __name__ == '__main__':
    cherrypy.quickstart(WebApp(), '/')

'''
6/6 TO-DO
where we left off:
- create searchType variable, and have passed it as parameter in functions that use it, now we just need to implement it accordingly in generate_query_results
onehotencoder:
- how to distinguish between words that onehotencoder has vs hasn't seen before
- query using the word that the user inputs??

'''