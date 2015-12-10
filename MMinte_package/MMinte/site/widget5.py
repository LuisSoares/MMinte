def getListOfModels():
    '''
    @summary: This function goes to the folder where all the mixed metabolic models are and creates a list of the model files  available. 
    '''
    import os
    
    
    path = '../userOutput/communityModels'
    listOfFiles = os.listdir(path)
    
    listOfModelsFile = open('../userOutput/communityModels/listOfModels.txt','w')
    listOfModels = []
    
    for file in listOfFiles:
        if file.endswith('.xml'):
            listOfModels.append(file)
            
    return listOfModels


def calculateGR(diet):
    
    
    import cobra
    
    
    growthRatesFile = open('../userOutput/growthRates.txt','a')
    growthRatesFileAlt = open('../userOutput/growthRatesAlt.txt','a')
    
    
    print>>growthRatesFile, 'FileName','\t','ObjFunctionSpeciesA','\t', 'ObjFunctionSpeciesB', '\t','GRSpeciesA', '\t','GRSpeciesB'
    print>>growthRatesFileAlt, 'FileName', '\t', 'ObjFuntionSpeciesA', '\t', 'ObjFunctionSpeceisB', '\t', 'GRSpeciesAFull','\t', 'GRSpeciesBFull','\t','GRASolo','\t','GRBSolo' 
    
    
    allModels = getListOfModels()
    
    for item in range(len(allModels)):
        
        '''
        @summary: load the model, all versions that will be manipulated in the analysis.
        '''
        fileName = allModels[item]
        modelFull = cobra.io.read_sbml_model('../userOutput/communityModels/%s' %allModels[item])
        modelMinusA = cobra.io.read_sbml_model('../userOutput/communityModels/%s' %allModels[item])
        modelMinusB = cobra.io.read_sbml_model('../userOutput/communityModels/%s' %allModels[item])
        
        
        '''
        @summary: get the reactions that make up the objective function for this model and put them in a list
        '''
        ObjKeys = modelFull.objective.keys()
        idObjKeys = ObjKeys[0].id, ObjKeys[1].id
        
        '''
        @summary: change the diet in all models.
        '''
        
        
        dietValues = open('../supportFiles/Diets.txt','r')
    
        '''
        @note: the diets file (Diets.txt) will have 4 possible diets. The fourth column will have the reactions whose bounds will be changed,
        the fifth column will have the value corresponding to the Complete diet, the sixth will have the values corresponding to the High fiber diet, 
        the seventh column will have the values corresponding to the Protein diet, and the eighth column will have the values corresponding to the western diet. 
        All these values were taken from the Thiele and Heinken AEM 2015 paper. The default diet will be Complete.
        '''
    
        for line in dietValues:
            try:
                new_line = line.rstrip('\n').split('\t')
                if diet == 'Complete':
                    modelFull.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[4])
                    modelMinusA.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[4])
                    modelMinusB.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[4])
                
                if diet == 'High Fiber':
                    modelFull.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[5])
                    modelMinusA.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[5])
                    modelMinusB.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[5])
            
                elif diet == 'Protein':
                    modelFull.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[6])
                    modelMinusA.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[6])
                    modelMinusB.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[6])
            
                elif diet == 'Western':
                    modelFull.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[7])
                    modelMinusA.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[7])
                    modelMinusB.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[7])
                
                elif diet == 'Other':
                    modelFull.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[8])
                    modelMinusA.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[8])
                    modelMinusB.reactions.get_by_id(new_line[3]).lower_bound = float(new_line[8])
                
            except:
                continue
        
        dietValues.close()
        
        '''
        @summary: run FBA on Full model
        '''
        modelFull.optimize()
        
        
        '''
        @summary: create the modelMinusA, that is, remove all reactions that are part of one of the species in the model.
        @summary: run FBA on that reduced model.
        '''
        
        listSilentItemsA = []
        
        for item in modelMinusA.reactions: #added MinusA to
            item = str(item)
            if item.startswith('modelA_'):
                listSilentItemsA.append(item)
        
        for j in listSilentItemsA:
            
            #try:
            rxn = j.strip()
            deadRxnA = modelMinusA.reactions.get_by_id(rxn)
            deadRxnA.remove_from_model()
            #except:
            #    continue
        
        
        modelMinusA.optimize()
        
        '''
        @summary: create the modelMinusA, that is, remove all reactions that are part of the other species in the model.
        @summary: run FBA on that reduced model.
        '''
        
        listSilentItemsB = []
        
        for item in modelMinusB.reactions:
            item = str(item)
            if item.startswith('modelB_'):
                listSilentItemsB.append(item)
        
        for j in listSilentItemsB:
            #try:
            rxn = j.strip()
            deadRxnB = modelMinusB.reactions.get_by_id(rxn)
            deadRxnB.remove_from_model()
            #except:
            #    continue
        
        
        modelMinusB.optimize()
        
        '''
        @summary: get the x_dict values for the reactions listed under idObjKeys for all three models.
        @summary: output them to a file where you are appending all this information. (when a reaction doesn't exist the output should be 
                a tag like "solo" or something).
                
        '''
        
        #ObjA = idObjKeys[0]
        #ObjB = idObjKeys[1]
        
        ObjA = []
        ObjB = []
        
        if idObjKeys[0].startswith('modelA'):
            ObjA = idObjKeys[0]
        else:
            ObjB = idObjKeys[0]
            
        
        if idObjKeys[1].startswith('modelB'):
            ObjB = idObjKeys[1]
        else:
            ObjA = idObjKeys[1]
        
        
        grAfull = modelFull.solution.x_dict[ObjA]
        grBfull = modelFull.solution.x_dict[ObjB]
        
        if ObjA in modelMinusA.solution.x_dict:
            grAMinusA = modelMinusA.solution.x_dict[ObjA]
        else:
            grAMinusA = 'Solo'
        
        
        if ObjB in modelMinusA.solution.x_dict:
            grBMinusA = modelMinusA.solution.x_dict[ObjB]
        else:
            grBMinusA = 'Solo'
        
        
        if ObjA in modelMinusB.solution.x_dict:
            grAMinusB = modelMinusB.solution.x_dict[ObjA]
        else:
            grAMinusB = 'Solo'
        
        
        if ObjB in modelMinusB.solution.x_dict:
            grBMinusB = modelMinusB.solution.x_dict[ObjB]
        else:
            grBMinusB = 'Solo'
        
        
        modelID = modelFull.id
        organisms = modelID.split('X')
        

        
        print>> growthRatesFile, fileName, '\t', organisms[0], '\t', organisms[1], '\t', grAfull,'\t', grBfull, '\n', fileName, '\t', organisms[0], '\t', organisms[1],'\t', grAMinusA,'\t', grBMinusA, '\n', fileName, '\t', organisms[0], '\t', organisms[1], grAMinusB,'\t', grBMinusB
        
        print>> growthRatesFileAlt, fileName, '\t', organisms[0], '\t', organisms[1], '\t', grAfull,'\t', grBfull,'\t',grAMinusB,'\t',grBMinusA 
    
    growthRatesFile.close()
