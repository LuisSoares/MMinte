def evaluateInteractions():
    '''
    @summary: open growth rates file and skip first line in calculations
    '''
    
    grFile = open('../userOutput/growthRatesAlt.txt', 'r')

    interactionsTableFile = open('../userOutput/interactionsTable.txt','a')
    
    print>> interactionsTableFile, 'Community file','\t','GenomeIDSpeciesA', '\t','GenomeIDSpeciesB','\t','GRSpeciesAFull','\t','GRSpeciesBFull','\t','GRASolo','\t','GRBSolo','\t','PercentChangeRawA','\t','PercentChangeRawB','\t', 'Type of interaction','\t','Code of interaction'
    
    next(grFile) #skip first line
    
    
    for item in grFile:
        
        item = item.replace("_",".")
        item = item.replace("A.","")
        item = item.replace(".model","")
        
        try:
            itemNew = item.split('\t')
            item = item.rstrip()
            '''
            @note: interactions calculations for species A
            '''
            percentChangeRawA = (float(itemNew[3])-float(itemNew[5]))/float(itemNew[5])

            '''
            @note: interactions calculations for species B
            '''
            percentChangeRawB = (float(itemNew[4])-float(itemNew[6]))/float(itemNew[6])
        
            '''
            @note: so what kind of interaction is it based on these calculations and the interactions listed in Thiele?
            '''
        
            typeOfInteraction = ''
            codeOfInteraction = ''
        
            if percentChangeRawA > 0.1 and percentChangeRawB > 0.1:
                typeOfInteraction = 'Mutualism'
                codeOfInteraction = 3
            elif percentChangeRawA > 0.1 and percentChangeRawB < -0.1:
                typeOfInteraction ='Parasistism'
                codeOfInteraction = 4
            elif percentChangeRawA > 0.1 and percentChangeRawB > -0.1 and percentChangeRawB < 0.1:
                typeOfInteraction = 'Comensalism'
                codeOfInteraction = 3
            elif percentChangeRawA < -0.1 and percentChangeRawB > 0.1:
                typeOfInteraction = 'Parasitism'
                codeOfInteraction = 4
            elif percentChangeRawA < -0.1 and percentChangeRawB < -0.1:
                typeOfInteraction = 'Competition'
                codeOfInteraction = 4
            elif percentChangeRawA < -0.1 and percentChangeRawB > -0.1 and percentChangeRawB < 0.1:
                typeOfInteraction = 'Amensalism'
                codeOfInteraction = 4
            elif percentChangeRawA > -0.1 and percentChangeRawA < 0.1 and percentChangeRawB > 0.1:
                typeOfInteraction = 'Comensalism'
                codeOfInteraction = 3
            elif percentChangeRawA > -0.1 and percentChangeRawA < 0.1 and percentChangeRawB < -0.1:
                typeOfInteraction = 'Neutralism'
                codeOfInteraction = 8
            elif percentChangeRawA > -0.1 and percentChangeRawA < 0.1 and percentChangeRawB > -0.1 and percentChangeRawB < 0.1:
                typeOfInteraction = 'Amensalism'
                codeOfInteraction = 4
            else:
                typeOfInteraction = 'Empty'
                codeOfInteraction = 2
        
        except:
            continue
        
        
        
        '''
        @todo: create the interactions table. See what the growth rates file looks like, and get the appropriate columns from there, 
        and merge the information with the finalTableTemp file.
        '''
        print>>interactionsTableFile, item,'\t', percentChangeRawA,'\t', percentChangeRawB, '\t', typeOfInteraction, '\t', codeOfInteraction
        '''
        @summary: besides assigning the interactions, the script works fine as long as there are no solo items in the lines (I removed them
        from the growthRates.txt file that was created just to see if this worked. And it does!!!).
        '''
        
    interactionsTableFile.close()
        
        
def createFinalTable():
    interactionsTableFile = open('../userOutput/interactionsTable.txt','r')
    finalTableTempFile = open('../userOutput/finalTableTemp.txt','r')
    
    interactionsTableFile.readline()
    finalTableTempFile.readline()



    interactionsTable = []
    for i in interactionsTableFile:
        i = i.rstrip()
        i = i.split()
        interactionsTable.append(i)
    
    
    
    finalTableTemp = []
    for i in finalTableTempFile:
        i = i.rstrip()
        i = i.split()
        finalTableTemp.append(i)
    

        finalTableFile = open('../userOutput/finalTable.txt','w')
        print>>finalTableFile, 'CommunityModel','\t','OtuIDA','\t','GenomeIDA','\t','OtuRowNumber','\t','OtuIDB','\t','GenomeIDB','\t','OtuRowNumber','\t','Correlation','\t','Interaction','\t','InteractionCode'
            
    for j in interactionsTable:
        for i in finalTableTemp:
            try:
                if float(i[1])==float(j[1]) and float(i[4])==float(j[2]):
                    print>>finalTableFile, j[0],'\t',i[0],'\t',i[1],'\t',int(i[2]),'\t',i[3],'\t',i[4],'\t',int(i[5]),'\t',float(i[6]),'\t',j[9],'\t',int(j[10])
                elif float(i[4])==float(j[1]) and float(i[1])==float(j[2]):
                    print>>finalTableFile, j[0],'\t',i[0],'\t',i[1],'\t',int(i[2]),'\t',i[3],'\t',i[4],'\t',int(i[5]),'\t',float(i[6]),'\t',j[9],'\t',int(j[10])
                else:
                    continue
            except:
                continue
                    
    finalTableFile.close()