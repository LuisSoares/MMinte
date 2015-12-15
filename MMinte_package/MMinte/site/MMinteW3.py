from spyre import server
from widget3 import getModels
import os
from os import listdir
from os.path import isfile, join

import cherrypy
cherrypy.config.update({"response.timeout":10000000,'log.access_file': '../supportFiles/logAccess_file.txt',
                        'log.error_file': '../supportFiles/logError_file.txt','log.screen':False})

class Widget3(server.App):
    title = 'Widget 3 '
    
    inputs = [{ "type":"text",
                "key":"genomeIDs",
                "label" : '<font size=4pt> Here we will be sending the genome IDs to <a href="http://modelseed.theseed.org/">ModelSEED</a> and getting a reconstructed and gap filled model from there. </font> <br>  <br> <font size=3pt>Tell me which file has the list of IDs for the Genomes for which you want to fetch metabolic models.</font>',
                "value":"../userOutput/ids4MS.txt"},
              ]
    
    outputs = [{"type":"html",
                "id":"some_html",
                "control_id":"run_widget",
                "tab":"Results",
                "on_page_load": False}]
    
    controls = [{"type":"button",
                 "label":"Run Widget 3",
                 "id":"run_widget"}]
    
    tabs = ["Results"]
    
    def getCustomCSS(self):
        ROOT_DIR = os.path.dirname(os.path.realpath('static/custom_styleMMinte.css'))
        with open(ROOT_DIR + '/custom_styleMMinte.css') as style:
            return style.read()+'''\n .right-panel{width:65%;margin: 1em}'''
        
        
    def getHTML(self,params):
        listIDs = params['genomeIDs']
        
        listOfModels = open(listIDs,'r')
        mypath =  '../userOutput/models'
        
        existingModels = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        
         
        for i in listOfModels:
            cherrypy.log("Will now see if %s is in the folder already" %i)
            i = i.rstrip()
            if (i + '.sbml') not in existingModels:
                cherrypy.log("The model %s isn't in the folder, so we're going to fetch it from ModelSeed" %i)
                try:
                    cherrypy.log("Started getting model for genome %s" %i)
                    getModels(i)
                    cherrypy.log("We finished getting the metabolic model for genome %s from ModelSEED." %i)
                except:
                    cherrypy.log("We were either unable to run getModels or were unable to get the metabolic models we wanted from ModelSEED. We'll keep going for now and try the next model.")
                    #return "Sorry something's wrong. Make sure the path to your file is correct."
                    pass
                continue
            else:
                cherrypy.log("The model %s was already in the folder" %i)
        
        ids = []
        idsFile = open('../userOutput/ids4MS.txt','r')
        
        
        for i in idsFile:
            ids.append(i)
            
        numIDs = len(ids)
        
        numModels = sum(os.path.isfile(os.path.join('../userOutput/models/', f)) for f in os.listdir('../userOutput/models/')) - 1

        
        return "You have %d genome IDs on the IDs file and %d models in the models folder. If you are still missing models, go ahead and run this widget again." %(numIDs,numModels)
    
if __name__ == '__main__':
    app = Widget3()
    app.launch()
