
def getUniqueOTU(corrs):
    
    '''
    @note: this function just gets all the different ids from the correlations file
    '''
    
    correlations = open(corrs,'r')
    OTUs = []
    for line in correlations:
        line = line.rstrip()
        line = line.split('\t')
        OTUs.append(line[0])
        OTUs.append(line[1]) #added this line November23, 2015
    
        uniqueOTUs = list(set(OTUs))

    return uniqueOTUs



    
def getSeqs(sequences):
  
    '''
    @note: this function cleans up the fasta file containing the representative OTUs sequences
    '''
    
    userSeqs = open(sequences,'r')
    reprOTUsfastaFile = open('../userOutput/representativeOTUs.fasta','w')
    seq = ''
    for line in userSeqs:
        if line.startswith('>'):
            seq += '+++++\n'
            seq += line
        else:
            seq += line.rstrip()
        
    
    seqs = seq.split('+++++\n')
    
    for i in seqs:
        print>>reprOTUsfastaFile, i
    
    userSeqs.close()
    reprOTUsfastaFile.close()
    
    return seqs



def workingOTUs(uniqueOTUs,seqs):
    '''
    @note: this function goes over the list of otu's we're actually going to use in the analysis and fetches their sequence from the full file of 
    representative OTUs
    '''
    
    reprOtusForAnalysis = open('../userOutput/reprOTUsToUse.fasta','w')

    for line in seqs:
        for item in uniqueOTUs:
            new_item = '>'+item+' '
            if line.startswith(new_item):
                print>>reprOtusForAnalysis, line
                '''
                @bug:  2 of the OTUs show up twice. I don't know why.
                '''
        
    reprOtusForAnalysis.close() 
    
