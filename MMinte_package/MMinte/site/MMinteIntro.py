from spyre import server
import io
import os


'''
With help from Luis Mendes Soares, Harvard Medical School
'''


#new stuff
import cherrypy
class custom_root(server.Root):
    @cherrypy.expose
    def image1(self, **args):
        import io
        buffer = io.BytesIO()
        ROOT_DIR = os.path.dirname(os.path.realpath('static/images/3485812-14.jpg'))
        f = open(ROOT_DIR+'/3485812-14.jpg','rb' )
        buffer.write(f.read())
        f.close()
        return buffer.getvalue()
    @cherrypy.expose
    def image2(self, **args):
        import io
        buffer = io.BytesIO()
        ROOT_DIR = os.path.dirname(os.path.realpath('static/images/flow.jpg'))
        f = open(ROOT_DIR+'/flow.jpg','rb' )
        buffer.write(f.read())
        f.close()
        return buffer.getvalue()

server.Root=custom_root
#end of new stuff
        
class Index(server.App):
    title='Intro'
    outputs = [{"output_type": "html",
                "output_id": "Index",
                "on_page_load": True}]
    
    def getCustomCSS(self):
        ROOT_DIR = os.path.dirname(os.path.realpath('static/custom_styleMMinte.css'))
        with open(ROOT_DIR + '/custom_styleMMinte.css') as style:
            return style.read()+'''\n .left-panel{display: none;}.right-panel{width:100%;margin:px;background: white;padding: 0px}'''
    
    
    def getHTML(self, params):

        return '''
<!-- Index page for MMinte app -->

    <head>
        <meta name="description" content="MMinte - Microbial metabolic interaction">
        <META NAME="ROBOTS" CONTENT="INDEX, FOLLOW">
    </head>
    
    <style>
        
        
        body {background-color: #f4f4f4;
                padding: 2em;
                margin-left:1em;
                margin-right:1em;
                margin-top:1em;
                margin-bottom:1em;
                border-radius: 10px;
        }
        
        
        
        h1.text {
            color: #00961E;
            text-align: center;
            font-family: "Arial";
            font-size: 3em;
            padding:0em;
        }
       
        p {color: black;
            text-align: justify;
            font-family: "Arial";
            font-size: 1.5em;
            line-height:1.2;
            text-indent: 2em;
            padding:1em;
        }
        
        h2 {
            text-indent: 2em;
            font-family: "Arial";
        }
        
        ul{
            text-align: justify;
            list-style-type:none;
            font-family: "Arial";
            font-size: 1.2em;
            line-height:1.3;
        }
        
        p.contact{font-size: 1.5em;
                font-family: "Arial";
                text-align: center;
                text-indent: 0em;
        }
                
        img.displayed {
                        width:65em;
                        height:27em;
                        display: block;
                        margin-left: auto;
                        margin-right: auto
        }
        
        img.flow{
                    width: 30em;
                    height: 45em;
                    float:right;
                    margin: 0 10px 10px 20px;
                    border: 2px solid black;
                    }
        
        a:link {color:black;
                text-decoration: none;
                }

        a:visited {text-decoration: none;
                }

        a:hover {text-decoration: underline;
                }

        a:active {text-decoration: underline;
                }    
    </style>
    

    <body>
    
   
    <img class="displayed" src='/image1' alt="MMinte logo" >
    
     <div>
    
    <h1 class="text">Welcome to MMinte!</h1>
    
    <h2>
        The least you need to know:
    </h2>
    <p>
        Systems Biology is an expanding field of research in the biological sciences. Its integrative approach requires the 
        collaboration between experts, and the use of tools, from fields that traditionally focus on specific levels of biological complexity.
        Enter <strong><font color=#00961E>MMinte - Microbial Metabolic interactions -</strong></font>, an application that allows researchers working on microbiome projects to predict the kinds of
        pairwise interactions between identified members of a community based on their metabolic models. With <strong><font color=#00961E>MMinte</strong></font>, users need only provide 
        a table containing pairs of operational taxonomic units (OTUs) that will be the focus of the analysis and representative sequences for those OTUs. 
        <strong><font color=#00961E>MMinte</strong></font> will then perform a series of sequential tasks to assess the kind of ecological interactions that are potentially 
        occurring between each two members of the community. The final output is a network diagram representing these interactions.
            
        <strong><font color=#00961E>MMinte</strong></font> is divided into 7 widgets with specific functions that may be used individually or sequentially. This modularity allows the 
        user to have better control of the workflow.
    </p>
    
    <h2>    
        The full description:
    </h2>
    
    <p>
        <strong><font color=#00961E>MMinte</strong></font> (pronounced /`minti/) is an integrated pipeline that allows users to explore the different kinds of pairwise interactions occurring 
        between members of a microbial community under different nutritional conditions. These interactions are predicted for the taxonomic units 
        of interest from as little information as the 16S dRNA sequences commonly obtained in studies describing the species membership of microbial 
        communities. Our application is composed of seven widgets that run sequentially, with each widget utilizing as the input file created in the
        previous widget as the default file for analysis. While <strong><font color=#00961E>MMinte</strong></font> may be run as a streamlined pipeline, due to its 
        compartmentalized nature, the user is given the ability to better control the full analysis. The user may choose to start the application 
        at any of the seven widgets, as long as the data provided has the adequate structure. The user also has access to the output files of each 
        widget (stored in the folder /userOutput). This allows the user to verify the quality of the data produced at each step of the analysis, 
        as well as explore it with alternative tools. 
    </p>
    
    <p>
        The widgets that make up <strong><font color=#00961E>MMinte</strong></font>, and the particular analysis they perform on the particular input files they take (see examples on folder 
        \supportFile\examples), are the following:
        
        <ul><img class="flow" src="/image2" alt="MMinte flow" >
        
        
 
            <li>
        <ins>Widget 1</ins> - Here, a table containing pairs of OTUs with some measure of association and a fasta file with sequences of representative 
        OTUs are used to create a .fasta file containing only16S dRNA sequences of the representative organisms that will be used in the subsequent 
        analysis.
            </li>
            
            <br>
            
            <li>
        <ins>Widget 2</ins> - A BLAST analysis against a local 16S dRNA database is run on the sequences present in the .fasta file with the OTU sequences to 
        be used in the analysis. This database was created from all the 16S dRNA sequences present in the PATRIC database as of November 2015 using 
        the NCBI command line tools (REF), and is provided to the user. It can be found in the folder /supportFiles. Various files are created from 
        this execution of this widget. Of note are the following: ids4MS.txt contains the NCBI Genome IDs for the organisms identified in the blast 
        analysis; pairsList.txt contains the pairs of organisms for which 2-species community models will be creates in Widget 4. Please note that 
        because several OTUs may be identified as belonging to the same species, the number of pairs listed will be smaller than the number of pairs 
        listed in the initial file provided by the user containing associated OTUs. The file cleanBlastOutput.txt lists the NCBI genome ID assigned 
        to each OTU provided by the user as well as the percent similarity between the genomic sequence of the particular OTU and the genome it was 
        assigned to.
            </li>
            
            <br>
            
            <li>
        <ins>Widget 3</ins> - In this step, the PATRIC website is accessed and the ModelSEED tools are used to reconstruct the models of the genomes listed in 
        the file ids4MS.txt. Every model reconstructed is then downloaded to the local machine in the Systems Biology Markup Language format (.sbml). 
            </li>

            <br>
            
            <li>
        <ins>Widget 4</ins> - The individual species models downloaded from PATRIC/ModelSEED are then used to create 2-species community models following the 
        directions in (REF). 
            </li>
            
            <br>
            
            <li>
        <ins>Widget 5</ins> - Following the procedure described in (REF), the python library cobrapy (REF) is then used to estimate the growth rates of each 
        species in the presence and absence of another species in the community for all 2-species community models created in the previous model. 
        Because the growth rate needs to be estimated under particular nutritional conditions, a Diets.txt file containing four kinds of diet is 
        provided to the user (in supportFiles/). The default diet used in the analysis is the complete diet, however, the user may choose between 
        this and "Western Diet", "High Fiber", "Protein Diet" or "Other". The last is so be defined by the user.
            </li>
        
            <br>
            
            <li>
        <ins>Widget 6</ins> - The growth rate values of each species in the full model (containing both species) or growing in isolation are then used to 
        assess the kind of interaction occurring between the species following the definitions listed in (REF).
            </li>
        
            <br>
            
            <li>
        <ins>Widget 7</ins> - A .json file is created to be used for plotting using D3 (REF). The information about the genetic similarity between the OTUs 
        provided by the user and the genome it was identified as is used to characterize the nodes of the network diagram. Information about the 
        level of association and kind of interactions predicted to be occurring between each pair of species is used to determine the edges between 
        each node in the network.
            </li>
    <br>
    
    
    </ul>
        
        
    </p>
    
    <p style="text-align:center">
        <strong><font color=#00961E>MMinte</strong></font> was developed by the Chia Lab at the Center for Individualized Medicine at the Mayo Clinic.
    </p>

    
    
    <h2 style="text-align:center"><ins>Contact and Suggestions:</ins></h2>

    <p class="contact"><a href="mailto:microbialmetabolicinteractions@gmail.com"><strong><font color=#00961E>MMinte</strong></font>'s awesome developers</a></p>
    
    </div>
    
    </body>
    '''


import cherrypy 

if __name__ == '__main__':
    app = Index()
    app.launch()