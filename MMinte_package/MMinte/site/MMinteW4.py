from spyre import server
from widget4 import totalEXRxns,createEXmodel,createReverseEXmodel, addEXMets2SpeciesEX, replaceRxns,replaceMets,createCommunityModel,createCommunityModel,allPairComModels
import os, os.path

import cherrypy
cherrypy.config.update({"response.timeout":1000000,'log.access_file': '../supportFiles/logAccess_file.txt',
                        'log.error_file': '../supportFiles/logError_file.txt','log.screen':False})

class Widget4(server.App):
    title = 'Widget 4'
    
    inputs = [{ "type":"text",
                "key":"listPairs",
                "label" : "<font size=4pt>In this widget we're just going to create 2-species community metabolic models.</font> <br> <br> <font size=3pt> Tell me where the file that has the list of pairs of genome IDs that will be in each 2-species community model is. If you don't specify where this file is, we'll just use the output form the previous Widget </font>",
                "value":"../userOutput/pairsList.txt"}
              ]
    
    outputs = [{"type":"html",
                "id":"some_html",
                "control_id":"run_widget",
                "tab":"Results",
                "on_page_load": False}]
    
    controls = [{"type":"button",
                 "label":"Run Widget 4",
                 "id":"run_widget"}]
    
    tabs = ["Results"]
    
    def getCustomCSS(self):
        ROOT_DIR = os.path.dirname(os.path.realpath('static/custom_styleMMinte.css'))
        with open(ROOT_DIR + '/custom_styleMMinte.css') as style:
            return style.read()+'''\n .right-panel{width:65%;margin: 1em}'''
        
        
    def getHTML(self,params):
        list = params['listPairs']
        try:
            allPairComModels(list)
            cherrypy.log("We're finished creating your community models")
        except:
            cherrypy.log("We were unable to run allPairComModels.")
            return "Sorry something's wrong. Make sure the path to your file is correct and that the python module cobrapy is loaded into your system."
            exit()
        
        
        numModels = sum(os.path.isfile(os.path.join('../userOutput/communityModels/', f)) for f in os.listdir('../userOutput/communityModels/')) - 1
        
        
        
        return "We created %d community models. In the next widget, we will use them  to predict the growth rate of their species in isolation and when in the community using COBRA tools. You can find all the models in the userOutput/communityModels folder." %numModels


if __name__ == '__main__':
    app = Widget4()
    app.launch()
