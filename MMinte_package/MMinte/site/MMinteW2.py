from spyre import server
from widget2 import blastSeqs, listTaxId4ModelSEED,otuGenomeIDCorrTable, uniq
import os

import cherrypy
cherrypy.config.update({"response.timeout":1000000,'log.access_file':'../supportFiles/logAccess_file.txt',
                        'log.error_file': '../supportFiles/logError_file.txt','log.screen':False})

class Widget2(server.App):
    title = 'Widget 2'
    
    inputs = [{ "type":"text",
                "key":"fastaFile",
                "label" : "<font size=4pt>Tell me which file has the sequences you want to get the genome ID for.</font>  <br>   <br> <font size=3p> If you don't change the file name, it will just use the output from the previous Widget </font>",
                "value":"reprOTUsToUse.fasta"},
              { "type":"text",
                "key":"corrsFile",
                "label" : "<font size=3pt>Remind me again which file has the correlations between OTUs...</font>",
                "value":"corrs.txt"}
              ]
    
    outputs = [{"type":"html",
                "id":"some_html",
                "control_id":"run_widget",
                "tab":"Results",
                "on_page_load": False}]
    
    controls = [{"type":"button",
                 "label":"Run Widget 2",
                 "id":"run_widget"}]
    
    tabs = ["Results"]
    
    def getCustomCSS(self):
        ROOT_DIR = os.path.dirname(os.path.realpath('static/custom_styleMMinte.css'))
        with open(ROOT_DIR + '/custom_styleMMinte.css') as style:
            return style.read()+'''\n .right-panel{width:65%;margin: 1em}'''
    
    def getHTML(self,params):
        try:
            seqsToBlast = params['fastaFile']
            corrs = params['corrsFile']
            try:
                blastSeqs(seqsToBlast)
                cherrypy.log("We finished blasting the sequences against the database with function blastSeqs.")
            except:
                cherrypy.log("We were unable to run blastSeqs.")
                return "Sorry something's wrong. Make sure the path to your file is correct."
                exit()
            
            try: 
                listTaxId4ModelSEED()
                cherrypy.log("We finished creating the list of genomeIDs we'll send to ModelSEED with the function listTaxId4ModelSEED.")
            except:
                cherrypy.log("We were unable to run listTaxId4ModelSEED.")
                return "Sorry something's wrong. Make sure the path to your file is correct."
                exit()
            
            
            try:    
                otuGenomeIDCorrTable(corrs)
                cherrypy.log("We finished creating a table with the correlations between the user gave in the beginning with the added information about the genomeID assigned to that particular OTU.")
            except:
                cherrypy.log("We were unable to run otuGenomeIDCorrTable.")
                return "Sorry something's wrong. Make sure the path to your file is correct."
                exit()
        
        except:
            cherrypy.log("We were unable to run this Widget.")
            return "Sorry something's wrong. Make sure the path to your file is correct and that the correct version of blast is installed."
        
        
        head = ["<strong><font color=#00961E size=4pt>Here's the genomeIDs we will use to reconstruct the metabolic models in the next widget:</strong></font>"]
        head.append('<br>')
        head.append("<strong><font color=#00961E size=2pt>You can find this and the other files created here in the userOutput folder.</strong></font>")
        head.append('<br>')
        
        myfile = open("../userOutput/ids4MS.txt",'r')
        
        for i in myfile:
            head.append('<br>')
            head.append(i)
        
        return head
    
if __name__ == '__main__':
    app = Widget2()
    app.launch()