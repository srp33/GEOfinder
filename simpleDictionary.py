import cherrypy

class TableWebApp:
    
    @cherrypy.expose
    def index(self):
        return ''' <html> 
        <head>
        <script>
        function toggleTable() {
            var table = document.getElementById("myTable");
            if (table.style.display === "none") {
                table.style.display = "block";
            } else {
                table.style.display = "none";
            }
        } 
        </script>
        </head>

        <body>
        <button onclick="toggleTable()">Generate</button>
        <table id="myTable" style="display:none">
            <tr>
                    <th>Header 1</th>
                    <th>Header 2</th>
                </tr>
                <tr>
                    <td>Data 1</td>
                    <td>Data 2</td>
                </tr>
        </table>
        </body>
        
        </html> '''

if __name__ == '__main__':
    cherrypy.quickstart(TableWebApp())

#hi anna this is abby :)