from spyre import server
from widget7 import createJSONforD3
import os
import webbrowser

import cherrypy
cherrypy.config.update({"response.timeout":1000000,'log.access_file': '../supportFiles/logAccess_file.txt',
                        'log.error_file': '../supportFiles/logError_file.txt','log.screen':False})

import cherrypy
class custom_root(server.Root):
    @cherrypy.expose
    def widget7_out(self):
		ROOT_DIR = os.path.dirname(os.path.realpath('index.html'))
		full_path = ROOT_DIR + '/index.html'
		with open(full_path) as data:
			return data.read()
    @cherrypy.expose
    def d3(self):
		ROOT_DIR = os.path.dirname(os.path.realpath('d3.v3.min.js'))
		full_path = ROOT_DIR + '/d3.v3.min.js'
		with open(full_path) as data:
			return data.read()
    @cherrypy.expose
    def data4plot_json(self):
		ROOT_DIR = os.path.dirname(os.path.realpath('data4plot_json'))
		full_path = ROOT_DIR + '/data4plot_json'
		with open(full_path) as data:
			return data.read()
			
server.Root=custom_root
			
	
class Widget7(server.App):
    title = 'Widget 7'
    
    inputs = [{ "type":"text",
                "key":"linksFile",
                "label" : "<font size=4pt> In this widget we'll create a json file that can be used by a D3 script to plot the network of interactions between your favorite organisms.</font> <br>   <br> <font size=3pt>Tell me which file has the full information of the analysis.</font>",
                "value":"../userOutput/finalTable.txt"},
              { "type":"text",
                "key":"nodesFile",
                "label" : "<font size=3pt> Also, tell me which file has the information about how close the OTU sequences were to the genome they we matched to.</font>",
                "value":"../userOutput/cleanBlastOutput.txt"}
              ]
    
    outputs = [{"type":"html",
                "id":"some_html",
                "control_id":"run_widget",
                "tab":"Results",
                "on_page_load": False}]
    
    controls = [{"type":"button",
                 "label":"Run Widget 7",
                 "id":"run_widget"}]
    
    tabs = ["Results"]
    
    def getCustomCSS(self):
        ROOT_DIR = os.path.dirname(os.path.realpath('static/custom_styleMMinte.css'))
        with open(ROOT_DIR + '/custom_styleMMinte.css') as style:
            return style.read()+'''\n .right-panel{width:65%;margin: 1em}'''
        
        
    def getHTML(self,params):
        links = params['linksFile']
        nodes = params['nodesFile']
        createJSONforD3(links,nodes)
        ROOT_DIR = os.path.dirname(os.path.realpath('index.html'))        
        full_path = ROOT_DIR + '/index.html'
        webbrowser.open_new_tab('http://localhost:8080/widget7_out')
        
        head = ["The plot with the network of interactions between your favorite organisms is shown on a new tab."]
        head.append('<br>')
        head.append('<br>')
        head.append('<br>')
        head.append("The shading of the nodes indicates how close the sequence of the OTU is to the sequence of the genome. The darker the node, the higher the similarity.")
        head.append('<br>')
        head.append('<br>')
        head.append('<br>')
        head.append("The length and thickness of the links reflect the association values on the initial file you provided. The shorter and thicker the link, the higher the association value.")
        head.append('<br>')
        head.append('<br>')
        head.append('<br>')
        head.append("The colors of the links reflect the kind of interaction. The red, green and grey represent negative, positive and no interaction, respectively.")
        head.append('<br>')
        head.append('<br>')
        head.append('<br>')
        head.append('<a href="http://d3js.org/" >D3 is awesome</a>! If you mouse over the nodes, you get the id of the OTU, and if you click a node and drag it, the network will follow it.')
        
        return head
        
        
        
        
         
        
if __name__ == '__main__':
    app = Widget7()
    app.launch()
