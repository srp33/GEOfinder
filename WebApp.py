# Final Copy
import cherrypy
import re 
#import simpleDictionary

class WebApp:

    @cherrypy.expose
    def index(self):
        #print(f"\n\n\n dictionary: \n\n\n {simpleDictionary}")
        return self.top_half_html()

    @cherrypy.expose
    def query(self, ids):
        return self.top_half_html(ids) + self.bottom_half_html(ids)

    #Internal:

    def top_half_html(self, ids = ""):
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
                name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)" rows="20" cols="50"></textarea>
            <button type="submit">Submit</button>
        </form>
            
        """
    #class="mt-3 subtitle is-3 has-text-centered"
    #class="content is-large has-text-black"
    #<input type="text" name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)">
    #rows="20" cols="50
    
    #<input type="text" name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)">
    def bottom_half_html(self, ids):
        return f"""
        <table class="content is-medium" id="myTable" border="1">
            <tr>
                <th>Data</th>
            </tr>
            {self.generate_table_rows(ids)}
        </table>
        </body>
        </html>
        """ 

    def generate_table_rows(self, ids):
        if (ids == ""):
            return ""
        rows = ""
        ids = ids.strip().upper()
        invalid = []
        for id in re.split(r"\n|,",ids):
            if not re.search(r"GSE\d+",id):
                invalid.append(id)
            else:
                rows += f"<tr><td>{id}</td></tr>"
        if invalid:
            return f"<h3>Sorry, the following IDs you entered were invalid: {invalid}</h3>"
        return rows
    
    


if __name__ == '__main__':
    cherrypy.quickstart(WebApp(), '/')


''' To-Do:
    - CSS: play around with Bulma more
    - look into how to import the python dictionary -  Convert Dct to dumps() (json pkg) - converts dct to str. Save json to file. 
        - webapp reads in json using loads() to convert to dct

    Later:
    - create vector database with chromadb. Access vec dbse after submit, display that info. Generate 100 vecs, size 100 (#s)

    Eventially:
    - file with data
'''
