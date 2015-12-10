
def totalEXRxns(modelA,modelB): 
    '''
    @attention: gave up on multiple arguments. Sticking with only 2 models, otherwise I won't have this done by next week.
    '''
    
    '''
    @summary: List all the exchange reactions in modelA
    '''
    
    EX_rxnsA = set()
    for i in range(len(modelA.reactions)):
        rxnsA = str(modelA.reactions[i])
        if 'EX_' in rxnsA:
            EX_rxnsA.add(rxnsA)
    
    '''
    @summary: List all the exchange reactions in modelB
    '''            
    EX_rxnsB = set()
    
    for j in range(len(modelB.reactions)):
        rxnsB = str(modelB.reactions[j])
        if 'EX_' in rxnsB:
            EX_rxnsB.add(rxnsB)
    
    '''
    @summary: list all the different exchange reactions that are present in models A and B. They will have some that overlap.
    '''
                   
    EX_total =  list(EX_rxnsA | EX_rxnsB)
    
    '''
    @summary: create a list with all the Exchange reactions and assign them a new identifier. These will be the exchange 
    reactions that will make up the external compartment that is common to both bacterial species.
    '''
    EX_finalRxns = []
    for each in range(len(EX_total)):
        rxn = EX_total[each] + '[u]'
        EX_finalRxns.append(rxn)
        
    return EX_finalRxns


def createEXmodel(EXreactions): 
    import cobra
    
    '''
    @summary: using the cobrapy package, create a brand new model that will contain the exchange reactions. This is the model
    we can manipulate when we want to change the nutrients available to the species. We will do this by changing either the
    upper or lower bounds (I don't remember and have to check). Ultimately we will create a file with a global exchange 
    reactions model that has a different diet associated with it. But this will require going over a whole bunch of models 
    to find all possible exchange reactions, and so I will stick to this approach for now.
    '''
    
    exchange_model = cobra.Model('Model with the exchange reactions only')
    
    for i in EXreactions: 
        new_i = str(i)
        new_i = new_i[3:]
        new_met = cobra.Metabolite(new_i)
        
        rxn = cobra.Reaction(i)
        rxn.lower_bound = -1000.000
        rxn.upper_bound = 1000.000
        rxn.objective_coefficient = 0.000
        rxn.add_metabolites({new_met:-1.0}) 
        
        exchange_model.add_reaction(rxn)
    
    return exchange_model 


def createReverseEXmodel(EXreactions): 
    import cobra
    
    '''
    @note: Ok, what was this about again?
    '''
    exchange_modelRev = cobra.Model('Model with the exchange reactions only with reversed stoi coefficient')
    for i in EXreactions: 
        new_i = str(i)
        new_i = new_i[3:]
        new_met = cobra.Metabolite(new_i)
        
        rxn = cobra.Reaction(i)
        rxn.lower_bound = -1000.000
        rxn.upper_bound = 1000.000
        rxn.objective_coefficient = 0.000
        rxn.add_metabolites({new_met:1.0})
        
        exchange_modelRev.add_reaction(rxn)
    
    return exchange_modelRev






def addEXMets2SpeciesEX(reverseEXmodel,speciesModel):    #this is working
    import cobra
    for j in range(len(reverseEXmodel.reactions)):
        exRxn = str(reverseEXmodel.reactions[j])
        
        for i in range(len(speciesModel.reactions)):
            rxn = str(speciesModel.reactions[i])
            if rxn in exRxn:
                new_met = reverseEXmodel.reactions[j].metabolites 
                speciesModel.reactions[i].add_metabolites(new_met)
                speciesModel.reactions[i].lower_bound = -1000.000
                speciesModel.reactions[i].upper_bound = 1000.000
     
    return speciesModel       
               
   
def replaceRxns(model,modelID):    
    import cobra
    
    '''
    @summary: Here we are just creating a new identifier for the reactions, so that we know which reactions come from one 
    species or the other. This is the same as assigning each species to a different compartment. This is important
    because the two species have common reactions and metabolites, but are not sharing these metabolites in their 
    biology, since the cells are closed compartments. They only share the metabolites that are transported in and out
    of the cell, hence the creation of an extra external compartment. 
    '''

    
    for i in range(len(model.reactions)):
        old_rxns = str(model.reactions[i])
        new_rxns = 'model' + modelID + '_' + old_rxns
        model.reactions[i].id = new_rxns

def replaceMets(model,modelID):
    import cobra
    
    '''
    @summary: Here we are just creating a new identifier for the metabolites, so that we know which reactions come from one 
    species or the other. This is the same as assigning each species to a different compartment. This is important
    because the two species have common reactions and metabolites, but are not sharing these metabolites in their 
    biology, since the cells are closed compartments. They only share the metabolites that are transported in and out
    of the cell, hence the creation of an extra external compartment. 
    '''
    
    for i in range(len(model.metabolites)):
        old_mets = str(model.metabolites[i])
        new_mets = 'model_' + modelID + '_' + old_mets
        
        model.metabolites[i].id = new_mets



def createCommunityModel(modelFileA, modelFileB):
    import cobra
    
    '''
    @note: record the date the community models were created
    '''
    
    
    '''
    @note: load the models using cobrapy.
    @param: modelFileA and modelFileB aren't really provided directly by the user but come from the listOfPairs of models that 
    are returned from the pairsOfModelsToMix function
    ''' 
    
    
    if modelFileA.endswith('.mat'):
        model1 = cobra.io.load_matlab_model('../userOutput/models/%s' %modelFileA)
    elif modelFileA.endswith('.xml') or modelFileA.endswith('.sbml'):
        model1 = cobra.io.read_sbml_model('../userOutput/models/%s' %modelFileA)
    elif modelFileA.endswith('.json'):
        model1 = cobra.io.load_json_model('../userOutput/models/%s' %modelFileA)
    

    #turn the file into a model in cobrapy
    if modelFileB.endswith('.mat'):
        model2 = cobra.io.load_matlab_model('../userOutput/models/%s' %modelFileB)
    elif modelFileB.endswith('.xml') or modelFileB.endswith('.sbml'):
        model2 = cobra.io.read_sbml_model('../userOutput/models/%s' %modelFileB)
    elif modelFileB.endswith('.json'):
        model2 = cobra.io.load_json_model('../userOutput/models/%s' %modelFileB)
    else:
        print "not able to find model %s" %modelFileB 
        
    
    '''
    @note: create a communityID to identify the output files belonging to each 2-species community created
    '''
    communityID = model1.id+ 'X' + model2.id
    
    
    '''
    @summary: get all the reactions identified as exchange reactions in both models you're mixing and create a list with of exchange 
    reactions. Then use this list to create what is called an exchange reaction model. This exchange reaction model will be the equivalente
    of an outside world model, or the lumen for instance, as in the Thiele models. Later manipulation of this particular model will allow
    the user to choose the diet under which the communities are growing.
    @param: the parameters used are defined in each function.  
    '''
    exModel = createEXmodel(totalEXRxns(model1, model2)) 
    
    '''
    @note: Output the exchange reactions created in the exchange reaction model for each 2-species model to a file so the user 
    can take a look at them. The user can uncomment if he/she wants this list.
    '''
    #exReactionsListU = open('../userOutput/%s/community%s_exRxnsU.txt' % (date, communityID),'w')
    #for i in range(len(exModel.reactions)):
    #    print>>exReactionsListU, exModel.reactions[i]
    
    #exReactionsListU.close()
    
    '''
    @summary: create a model that has the fluxes of the exchange reactions reversed. This is because these reactions will will added
    specifically to each species, in the model. So we are extending the original species models to have more reactions so that each species
    can exchange metabolites with exchange reactions model. The exchange reactions models then becomes a comparment shared by all the other 
    species in the community model. This is what will allow us to determine how the species interact when they have to share resources.
    '''
    revEXmodel = createReverseEXmodel(totalEXRxns(model1, model2)) 
    
    '''
    @note: I don't remember why these are here...
    '''
    
    replaceMets(model1,'A')
    replaceMets(model2,'B')
 
    new_m1 = addEXMets2SpeciesEX(revEXmodel,model1) 
    new_m2 = addEXMets2SpeciesEX(revEXmodel,model2) 

    replaceRxns(new_m1,'A')
    replaceRxns(new_m2,'B')
    
    
    '''
    @note: Output the all the reactions for species A and for specie B in the model to a file so the user can take a look at them. 
    If the user wants this, the user can uncomment the script here. I will leave it as is becasue otherwise we will get a whole bunch of
    files that are not useful for our analysis or growth rate.
    '''
    #ReactionsListA = open('../userOutput/%s/community%s_Rxns%s.txt' % (date, communityID ,model1.id), 'w')
    #for i in range(len(model1.reactions)):
    #    print>>ReactionsListA, model1.reactions[i]
    
    #ReactionsListA.close()
  
    #ReactionsListB = open('../userOutput/%s/community%s_Rxns%s.txt' % (date, communityID ,model2.id), 'w')
    #for i in range(len(model2.reactions)):
    #    print>>ReactionsListB, model2.reactions[i]
    
    #ReactionsListB.close() 
    
    
    '''
    @note: This part is where the community model actually gets created. All previous steps were changing the models that will be put 
    together in the community so that the reactions and metabolites for each organism can still be distinguished and there is
    proper compartmentalization of reactions and metabolites.
    
    @note: because you can't really create a model from the sum of other 2, I just created a new model (mix) that is exactly model1. The 
    alternative would have been to create an empty model, then add the reactions and metabolites of model1, model2, and exModel.
    '''
    
    mix = new_m1 #maybe need to copy(new_m1)
    mix.id = communityID
    mix.add_reactions(new_m2.reactions)
    mix.add_metabolites(new_m2.metabolites)
    mix.add_reactions(exModel.reactions)
    mix.add_metabolites(exModel.metabolites)

    '''
    @note: Then just output the newly created community model to its folder. The models should then be ready to be further analyzed on
    widget5
    '''
    cobra.io.write_sbml_model(mix, "../userOutput/communityModels/community%s.xml" %communityID)
   

    

def allPairComModels(listOfPairs):
    
    import os
    '''
     @summary: This function creates all possible 2-species community models given a list of models.
     @note: First check if the directory exists. If it doesn't, create it.
    '''
    
    
    newpath = r'../userOutput/' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    pairsListFile = open(listOfPairs,'r')
    pairsListFile.readline()
    
    pairsList = []
    
    for i in pairsListFile:
        i = i.rstrip()
        i = i.replace("'","")
        i = i.split()
        pairsList.append(i)
    
    
    for i in range(len(pairsList)):
        modelA = '%s.sbml' %pairsList[i][0]
        modelB = '%s.sbml' %pairsList[i][1]
        try:
            createCommunityModel(modelA,modelB)
        except:
            continue
    
    
    pairsListFile.close()
        
