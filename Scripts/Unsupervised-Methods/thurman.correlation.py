import sys
from scipy import stats

def Calculate_Correlation(array1, array2):
    stat=stats.pearsonr(array1, array2)[0]
    return stat

def Create_Gene_Dict(genes):
    geneDict={}
    for line in genes:
        line=line.rstrip().split("\t")
        if line[6] not in geneDict:
            geneDict[line[6]]=[line[3]]
        else:
            geneDict[line[6]].append(line[3])
    return geneDict

def Process_Data(data):
    dataDict={}
    for line in data:
        line=line.rstrip().split("\t")
        dataDict[line[0]]=[float(i) for i in line[1:]]
    return dataDict

tssData=open(sys.argv[1])
tssDict=Process_Data(tssData)
tssData.close()

elsData=open(sys.argv[2])
elsDict=Process_Data(elsData)
elsData.close()

genes=open(sys.argv[3])
geneDict=Create_Gene_Dict(genes)
genes.close()


pairs=open(sys.argv[4])

for line in pairs:
    line=line.rstrip().split("\t")
    els=line[0]
    tss=geneDict[line[1]]
    corArray=[]
    for t in tss:
        cor=Calculate_Correlation(elsDict[els],tssDict[t])
        corArray.append(cor)
        
    print line[2], "\t", max(corArray), "\t", els, "\t", line[1]
    
    
pairs.close()
        
    
