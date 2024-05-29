import cherrypy

#https://www.w3schools.com/tags/att_input_type_checkbox.asp 
#where i was learning about checkboxes, to be checked next time :)

class test:

    # <button onclick="toggleTable()">Generate</button>

    def process_metadatas(self, species, num_samples, platform):
        return {  
            "Species": [val for val in species if val],
            "Num Samples": [val for val in num_samples if val],
            "Platform": [val for val in platform if val] 
        }

    # a) 1-10, b) 11-50, c) 51-100, d) 101-500, e) 501-1000, f) 1000+
    @cherrypy.expose
    def query(self, human="", mouse="", rat="", a="", b="", c="", d="", e="", f="", rnaSeq="", microarr=""):
        # return self.results()
        metadatas = self.process_metadatas([human, mouse, rat], [a, b, c, d, e, f], [rnaSeq, microarr])
        return f'''
        <h1>Results {metadatas}</h1>
        </body>
        </html>
        '''
    
    @cherrypy.expose
    def index(self):
        return f''' 
        <html> 
        <link 
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css"
        >
        <body>

        <h1 class="mt-3 subtitle is-3 has-text-centered is-family-sans-serif">Filters:</h1>
        <form action="/query">
            <p class="mgh-medium">
            <div class="columns">
                <div class="column"><strong>Species:</strong><br>
                    <input type="checkbox" id="human" name="human" value="human">
                    <label for="vehicle1">Human</label><br></p>
                    <input type="checkbox" id="mouse" name="mouse" value="mouse">
                    <label for="mouse">Mouse</label><br>
                    <input type="checkbox" id="rat" name="rat" value="rat">
                    <label for="rat">Rat</label><br><br>
                </div>
                <div class="column"><strong># Samples:</strong><br>
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
                <div class="column"><strong>Platform:</strong><br>
                    <input type="checkbox" id="rnaSeq" name="rnaSeq" value="RNA sequencing">
                    <label for="rnaSeq">RNA Sequencing</label><br></p>
                    <input type="checkbox" id="microarr" name="microarr" value="Microarrays">
                    <label for="microarr">Microarrays</label><br><br><br><br><br><br>
                    <input type="submit" value="Submit" style="font-size:18px">
                </div>
            </div>        
        </p>        
        </form>


        
        '''

    def results(self):
        print("in the results function")


if __name__ == '__main__':
    cherrypy.quickstart(test())