def createJSONforD3(links,nodes):
    
    import json
    
    '''
    @note: the files that will be used for this script are actually going to be the cleanBlastOutput output of widget 1) and the 
    finalTable (output of widget6).
    '''
    
    
    '''
    @summary: now we create the links part of the json file.
    '''
    linksFile = open(links,'r')
    
    linksFile.readline()
    
    linksTable = []
    
    for i in linksFile:
        i = i.rstrip()
        i = i.split('\t')
        
        if float(i[7]) == 1:
            closeness = 1
        elif float(i[7]) > 0.95:
            closeness = 2
        elif float(i[7]) > 0.9:
            closeness = 3
        else:
            closeness = 10
        
        new_line = i[0].rstrip(), i[1].rstrip(),i[2].rstrip(),i[3].rstrip(),i[4].rstrip(),i[5].rstrip(),i[6].rstrip(),i[7].rstrip(),closeness,i[8].rstrip(),i[9].rstrip()        
        linksTable.append(new_line)
        
    link_value = []
    
    

    for i in linksTable:
        new_link = {"source":int(i[3]),"target":int(i[6]),"value":int(i[8]),"interaction":int(i[10])}
        link_value.append(new_link)
    
    listOfOTUs = []
    for i in linksTable:
        listOfOTUs.append(i[1].rstrip())
        listOfOTUs.append(i[4].rstrip())
        
    listOfOTUs = list(set(listOfOTUs)) 
    '''
    @summary: lets first create the nodes part of the json file
    '''
    nodesFile = open(nodes,'r')
    #nodesFile = open('../userOutput/cleanBlastOutput.txt','r')
    nodesFile.readline()
    
    nodesTable = []
    
    for i in nodesFile:
        i = i.rstrip()
        i = i.split()
        nodesTable.append(i)
    
    node_value = []
        
    for i in nodesTable:
        if i[1] in listOfOTUs:
            new_node = {'name':i[1],'group':int(i[4])}
            node_value.append(new_node)
        else:
            continue
        
    '''
    @bug: now the row numbers are wrong...
    '''
    
        
    '''
    @summary: put the nodes values and the links values into the final dataset that is in the dictionary format
    ''' 
    dataDict = {'nodes': node_value, 'links': link_value}



    '''
    @summary: dump the new data into a json file
    '''
    
    with open('data4plot_json','w') as outfile:
        json.dump(dataDict, outfile)
        
        