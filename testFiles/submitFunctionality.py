import cherrypy

class test:

    # <button onclick="toggleTable()">Generate</button>
    
    @cherrypy.expose
    def index(self):
        return ''' <html> 
        <head></head>
        <body>

        <textarea id="user_input" class="content is-medium textarea has-fixed-size textarea is-hovered textarea is-info"
        name="ids" placeholder="Enter IDs (ie. GSE123, GSE456)" rows="10" oninput="check_input()"></textarea>
        <button id="submit_button" class="button is-info" type="submit" onclick="submit_form()" disabled>Submit</button>

        <script>
        <!-- comment :) -->
        function check_input() {
                var input = document.getElementById('user_input').value;
                var button = document.getElementById('submit_button');
                button.disabled = input === '';
        } 
        function submit_form() {
            // Disable the submit button
            var button = document.getElementById('submit_button');
            var textarea = document.getElementById('user_input');
            button.disabled = true;
            textarea.value = "";
            textarea.placeholder = "loading results..."
            // call other function that's supposed to be called 
        }
        </script>
        </body>
        </head>
'''
    
    # process input (whether or not name was input)
    @cherrypy.expose
    def getName(self, name=""):
        pass

if __name__ == '__main__':
    cherrypy.quickstart(test())

#use jquery, change button type to "button" + remove form tag so that we can have multiple buttons with functionality 