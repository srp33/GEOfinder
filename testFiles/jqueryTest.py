import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>jQuery Example</title>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        </head>
        <body>

        <button>Click me</button>
        <p>This paragraph will be hidden when you click the button.</p>

        <script>
            $(document).ready(function(){
                $('button').click(function(){
                    $('p').hide();
                });
            });
        </script>

        </body>
        </html>
        """

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())

