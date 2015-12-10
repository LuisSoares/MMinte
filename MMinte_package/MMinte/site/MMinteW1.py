from spyre import server
from widget1 import getUniqueOTU, getSeqs, workingOTUs
import os

import cherrypy
cherrypy.config.update({"response.timeout":1000000,'log.access_file': '../supportFiles/logAccess_file.txt',
                        'log.error_file': '../supportFiles/logError_file.txt','log.screen':False})

class Widget1(server.App):
    title = '<h1><font color=black size=4em>Widget 1</font></h1>'
    
    inputs = [{ "type":"text",
                "key":"text1",
                "label" : "<font size=4pt>In this widget we're just going to create a file with the sequences of the OTUs that will be required for the rest of the analysis.</font> <br> <br> <font size=3pt>Tell me which file has the information about associated OTUs</font>",
                "value":"../userFiles/corrs.txt"},
              {"type":"text",
                "key":"text2",
                "label" : "<font size=3pt>Tell me which file has the sequences of the representative OTUs</font>",
                "value":"../userFiles/otus.fasta"}
              ]
    
    outputs = [{"type":"html",
                "id":"some_html",
                "control_id":"run_widget",
                "tab":"Results",
                "on_page_load": False}]
    
    controls = [{"type":"button",
                 "label":"Run Widget 1",
                 "id":"run_widget"}]
    
    tabs = ["Results"]
    
    
    def getCustomCSS(self):
        ROOT_DIR = os.path.dirname(os.path.realpath('static/custom_styleMMinte.css'))
        with open(ROOT_DIR + '/custom_styleMMinte.css') as style:
            return style.read()+'''\n .right-panel{width:65%;margin: 1em}'''
    

        
        
    def getHTML(self,params):
        corrsFile = params['text1'] 
        sequencesFile = params['text2']
        
        try:
            corrs = getUniqueOTU(corrsFile)
            cherrypy.log("We successfully ran getUniqueOTU.")
        except:
            cherrypy.log("We were unable to run getUniqueOTU.")
            return "Sorry something's wrong. Make sure the path to your file is correct."
            exit()
        
        try:
            seqs = getSeqs(sequencesFile)
            cherrypy.log("We successfully ran getSeqs.")
        except:
            cherrypy.log("We were unable to run getSeqs.")
            return "Sorry something's wrong. Make sure the path to your file is correct."
            exit()
        
        
        try:
            workingOTUs(corrs,seqs)
            cherrypy.log("We successfully ran workingOTUs.")
        except:
            cherrypy.log("We were unable to run workingOTUs.")
            return "Sorry something's wrong. Make sure the path to your file is correct."
            exit()
        
        
        head = ["<strong><font color=#00961E size=4pt>Here are the OTU's that will be used in the rest of the analysis:</strong></font>"]
        head.append('<br>')
        head.append("<strong><font color=#00961E size=2pt>You can find the full sequences in the userOutput folder.</strong></font>")
        head.append('<br>')
        
        myfile = open("../userOutput/reprOTUsToUse.fasta")
        
        for i in myfile:
            if i.startswith('>'):
                head.append('<br>')
                head.append(i)
                
       
        return head
        
        
if __name__ == '__main__':
    app = Widget1()
    app.launch()