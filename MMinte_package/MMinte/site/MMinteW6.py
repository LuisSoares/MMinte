from spyre import server
from widget6 import evaluateInteractions,createFinalTable
import os

import cherrypy
cherrypy.config.update({"response.timeout":1000000,'log.access_file': '../supportFiles/logAccess_file.txt',
                        'log.error_file': '../supportFiles/logError_file.txt','log.screen':False})

class Widget6(server.App):
    title = '<h1><font color=black size=4em> Widget 6 </font></h1>'
    
    inputs = [{ "type":"text",
                "key":"words",
                "label" : "<font size=4pt>Here we will look at the much the growth rates of each species changes due to the presence of a partner in a community, and the direction of this change. We then label the interaction as either positive, negative, or no interaction</font> <br>   <br> <font size=3pt> We don't really need any information from you but you're welcome to introduce yourself. You still have to click the button though.</font>",
                "value":""}
              ]
    
    outputs = [{"type":"html",
                "id":"some_html",
                "control_id":"run_widget",
                "tab":"Results",
                "on_page_load": False}]
    
    controls = [{"type":"button",
                 "label":"Run Widget 6",
                 "id":"run_widget"}]
    
    tabs = ["Results"]
    
    def getCustomCSS(self):
        ROOT_DIR = os.path.dirname(os.path.realpath('static/custom_styleMMinte.css'))
        with open(ROOT_DIR + '/custom_styleMMinte.css') as style:
            return style.read()+'''\n .right-panel{width:65%;margin: 1em}'''
    
    def getHTML(self,params):
        
        
        try:
            cherrypy.log("We are starting the evaluation of interactions between pairs of organisms")
            evaluateInteractions()
            cherrypy.log("Finished evaluating the interactions between the pairs of organisms")
        except:    
            cherrypy.log("We were unable to run evaluateInteractions.")
            return "Sorry something's wrong. Make sure the path to your file is correct."
            exit()
        
        
        try:
            cherrypy.log("We will create the final table ")
            createFinalTable()
            cherrypy.log("Finished creating the final table ")
        except:    
            cherrypy.log("We were unable to run evaluateInteractions.")
            return "Sorry something's wrong. Make sure the path to your file is correct."
            exit()
            
            
        
        name = params['words']
        
        
        head = ["<strong><font color=#00961E size=4pt>Hi %s! Here's a glimpse of what the first few lines of your Final Table look like.</strong></font>" %name]
        head.append("<strong><font color=#00961E size=4pt> This table has all the information you need to do further analysis regarding the interactions on these species</strong></font>")
        head.append('<br>')
        head.append("<strong><font color=#00961E size=2pt>You can find this and the other files created here in the userOutput folder.</strong></font>")
        head.append('<br>')
        
        
        
        with open("../userOutput/finalTable.txt",'r') as myfile:
            top = [next(myfile) for x in xrange(10)]
        
        for i in top:
            head.append('<br>')
            head.append(i)
            
        return head
        
if __name__ == '__main__':
    app = Widget6()
    app.launch()