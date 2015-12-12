from spyre import server
from widget5 import getListOfModels,calculateGR
import os

import cherrypy
cherrypy.config.update({"response.timeout":1000000,'log.access_file': '../supportFiles/logAccess_file.txt',
                        'log.error_file': '../supportFiles/logError_file.txt','log.screen':False})

class Widget5(server.App):
    title = 'Widget 5'
    
    inputs = [{ "type":"dropdown",
                "key":"diet",
                "label" : "<font size=4pt>Now we're going to calculate growth rates for the species in each community. Because we will want to know how the presence of another species in the community affect the growth of a particular organism, we will estimate how the species growth when in the absence and presence of another species in the community under particular nutritional conditions. </font>. <br>      <br> <font size=3pt> You can determine which kind of metabolites are available for the organisms by choosing a diet </font>",
                "options" : [ {"label": "Complete", "value":"Complete"},
                            {"label": "High Fiber", "value":"High Fiber"},
                            {"label": "Protein", "value":"Protein"},
                            {"label":"Western","value":"Western"},
                            {"label":"Other","value":"Other"}],
                "value":'Complete'}
              ]
    
    outputs = [{"type":"html",
                "id":"some_html",
                "control_id":"run_widget",
                "tab":"Results",
                "on_page_load": False}]
    
    controls = [{"type":"button",
                 "label":"Run Widget 5",
                 "id":"run_widget"}]
    
    tabs = ["Results"]
    
    def getCustomCSS(self):
        ROOT_DIR = os.path.dirname(os.path.realpath('static/custom_styleMMinte.css'))
        with open(ROOT_DIR + '/custom_styleMMinte.css') as style:
            return style.read()+'''\n .right-panel{width:65%;margin: 1em}'''
    
    def getHTML(self,params):
        food = params['diet']
        
        try:
            cherrypy.log("We are starting the growth rate calculation")
            calculateGR(food)
            cherrypy.log("Finished calculating the growth rates of the species")
        except:
            cherrypy.log("We were unable to run calculateGR.")
            return "Sorry something's wrong. Make sure the path to your file is correct."
            exit()
         
        
        head = ["<strong><font color=#00961E size=4pt>Here's a glimpse of what the first few lines of your growth rates file look like.</strong></font>"]
        head.append('<br>')
        head.append("<strong><font color=#00961E size=2pt>You can find this and the other files created here in the userOutput folder.</strong></font>")
        head.append('<br>')
        
    
        
        with open("../userOutput/growthRates.txt",'r') as myfile:
            top = [next(myfile) for x in xrange(10)]
        
        for i in top:
            head.append('<br>')
            head.append(i)
           
            
        return head

if __name__ == '__main__':
    app = Widget5()
    app.launch()