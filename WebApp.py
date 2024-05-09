# Final Copy
import cherrypy

class WebApp:

    @cherrypy.expose
    def index(self):
        return self.top_half_html()

    @cherrypy.expose
    def query(self, ids):
        return self.top_half_html(ids) + self.bottom_half_html(ids)

    #Internal:

    def top_half_html(self, ids = ""):
        return f"""
        <html>
        <head></head>
        <body>
        <h1>Enter GEO Accession IDs:</h1>
        <form action="/query" method="post">
            <input type="text" name="ids" value = "{ids}" placeholder="Enter IDs (ie. GSE123, GSE456)">
            <button type="submit">Add Data</button>
        </form>
        """
    
    def bottom_half_html(self, ids):
        return f"""
        <table id="myTable" border="1">
        <!-- table id="myTable" style="display:none" border="1" -->
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
        for d in ids.split(","):
            rows += f"<tr><td>{d}</td></tr>"
        return rows
    


if __name__ == '__main__':
    cherrypy.quickstart(WebApp(), '/')


''' To-Do:
    - make text area
    - check valid inputs. Allow "," and "\n".
    - CSS: (Tail Wind or) Bulma.io. Installation: cdn + head tag
    - Simple separate py script to gen Dict. Key=GSE, Val=dct. Inner dct: k,v with dataset features. Convert Dct to dumps() (json pkg) - converts dct to str. Save json to file. 
        - webapp reads in json using loads() to convert to dct

    Later:
    - create vector database with chromadb. Access vec dbse after submit, display that info. Generate 100 vecs, size 100 (#s)

    Eventially:
    - file with data
'''
