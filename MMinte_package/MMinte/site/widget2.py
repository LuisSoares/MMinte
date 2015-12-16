

def blastSeqs(fastaFile):
    from Bio.Blast.Applications import NcbiblastnCommandline
    
    '''
    @summary: define the files that will be used in the blast process. These should be an input file, an output file, and the local
    database to be used. The database provided in version1 of Bug contains the 16S sequences for all bacteria present in the PATRIC 
    database as of 3 November 2015 (provided by Maulik Shukla)
    '''
    
    dbase = '../supportFiles/16Sdb'
    outputFile = '../userOutput/blastOutput.txt'
    
    '''
    @summary: run a local blast of the user's representative OTUs, the output format is tabular, only one match is shown
    '''
    blastn_cline = NcbiblastnCommandline(cmd='../ncbi-blast-2.2.22+/bin/blastn', query= fastaFile, db= dbase, outfmt= 6, out= outputFile, max_target_seqs = 1)
    stdout = blastn_cline()
    

    
def listTaxId4ModelSEED():
    '''
    @summary: once the blast run is done, we'll process the output so that it creates two files: one is the list of models that will be created
    using ModelSeed (ids4MS.txt); the other is an informative file to the user that will have the representative otu id, it's abundance, the species it 
    corresponds to, and the percent identity between the query otu sequence, and the sequence in the database (cleanBlastOutput.txt).
    '''
    
    blastResultsFile = open('../userOutput/blastOutput.txt', 'r')
    cleanBlastResultsFile = open('../userOutput/cleanBlastOutput.txt','w')
    print>>cleanBlastResultsFile, 'Row number', '\t', 'Query_Otu_ID','\t','Species_ID','\t' ,'Percent_ID', '\t', 'Similarity Group'
    
    
    ids4MSFile = open('../userOutput/ids4MS.txt', 'w')
    
    ids4MS = []
    blastTable = []
    
    
    
    
    for i in blastResultsFile:
        item = i.split()
        ids4MS.append(item[1])
        blastTable.append(item)
        
    '''
    @note: assign a similarity group tag to each otu so that the nodes have a different color depending on percent similarity to the 16S dRNA sequence of the genome used to create the closest
    metabolic model
    '''
    
      
    cleanBlastResultsTable = []    
    uniqueRows = []    
    
    for x in blastTable:
        if x[0] not in uniqueRows:
            cleanBlastResultsTable.append(x)
            uniqueRows.append(x[0])

    
    counter = 0 
    
    for i in cleanBlastResultsTable:
        
        similarityGroup = ''
            
        if float(i[2]) >= 95:
            similarityGroup = '9'
        elif float(i[2]) >= 80:
            similarityGroup = '10'
        elif float(i[2]) >= 50:
            similarityGroup = '11'
        else:
            similarityGroup = '12'
        
        '''
        @todo: need to find a way to not have duplicate entries in clean output
        '''
        
        print>>cleanBlastResultsFile, counter, '\t',i[0],'\t',i[1],'\t',i[2], '\t', similarityGroup
        
        counter += 1
    
    cleanIds4MS=list(set(ids4MS))
    
    blastResultsFile.close()
    
    for i in cleanIds4MS:
        print>>ids4MSFile, i
    
    ids4MSFile.close()
    cleanBlastResultsFile.close()

'''
    @attention: The functions defined below were written so that a table close to the final table containing the pairs of species, their 
    correlation values and interaction is created.
    
    @note: The way the script is written now, a  bunch of repeated entries are created (no, I don't know why), 4 for each entry to be more 
    precise. The function below seems to work to just get the unique entry
'''  

def uniq(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)
  return output


'''
    @summary: function that starts creating the output file needed to feed into the network plotting, towards the end, the type of interactions will
    be added to this table. That file is also required to create the pairs of models.
'''

def otuGenomeIDCorrTable(corrsFile):
    
    '''
    @note: get the files that contain the information to create the table
    '''
    corrsTableFile = open(corrsFile, 'r')
    blastOutputFile = open('../userOutput/cleanBlastOutput.txt', 'r')


    '''
    @note: open a file where it will all be dumped.
    '''
    pairsListFile = open('../userOutput/pairsList.txt', 'w')
    finalTableFile = open('../userOutput/finalTableTemp.txt','w')
    print>>pairsListFile, 'OtuAGenomeID','OTUBGenomeID'
    print>>finalTableFile, 'OtuAQueryID', '\t','OtuAGenomeID', '\t','OtuARowNumber','\t','OtuBQueryID','\t', 'OtuBGenomeID','\t', 'OtuBRowNumber', '\t','CorrCoefficient'

    '''
    @note: fast hack to remove the first line of the files because everything else is numeric and it makes my life so much easier.
    '''
    corrsTableFile.readline()
    blastOutputFile.readline()


    '''
    @note: create some empty tables to transfer the data from the files to. And then put the data from the files in the tables.
    '''
    
    corrsTable = []
    blastOutput = []
    
    

    for i in corrsTableFile:
        i = i.rstrip()
        i = i.split()
        corrsTable.append(i)

    for i in blastOutputFile:
        i = i.rstrip()
        i = i.split()
        blastOutput.append(i)
    
    
    '''
    @note: this is the first temporary table that will have part of the information that will be needed to create the last file. the loop
    deals with the first column of OTUs and the loop creates an extra column that has the genome ID corresponding to that Otu
    '''
    pairsListTemp = []



    for i in corrsTable:
        for j in blastOutput:
            if str(i[0]) == str(j[1]):
                new_item = [i[0], j[2], j[0], i[1], i[2]]
                pairsListTemp.append(new_item)
            
            
    '''
    @note: this is the second temporary table that will have part of the information that will be needed to create the last file. the loop
    deals with the second column of OTUs and the loop creates an extra column that has the genome ID corresponding to that Otu
    '''
    pairsListTemp2 = []
    finalTableTemp = []

    for i in pairsListTemp:
        for j in blastOutput:
            if str(i[3]) == str(j[1]):
                finalTableTemp.append([i[0], i[1], i[2], i[3], j[2], j[0], i[4]])
                pairsListTemp2.append([i[1],j[2]])
            


    '''
    @note: remove the duplicate entries
    '''
    finalTable = uniq(finalTableTemp)
    pairsList = uniq(pairsListTemp2)
    
    '''
    @note: put everything in that final table.
    '''
    for i in pairsList:
        print>>pairsListFile, i[0].rstrip(),i[1].rstrip()
        
    for i in finalTable:    
        print>>finalTableFile, i[0].rstrip(),'\t', i[1].rstrip(),'\t',i[2].rstrip(),'\t',i[3].rstrip(),'\t',i[4].rstrip(),'\t',i[5].rstrip(), '\t', i[6].rstrip()
    
    pairsListFile.close()
    finalTableFile.close()
    
'''
@summary: run all functions
'''

