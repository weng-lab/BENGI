import sys, scipy, math
from scipy import stats

def Process_Biosample(biosample):
    biosampleDict={"GM12878":28, "HeLa":50, "K562":88,"HMEC":59,"NHEK":100}
    if biosample in biosampleDict:
        return biosampleDict[biosample]
    else:
        return "no"

def Calculate_Correlation(array1, array2):
    stat=stats.pearsonr(array1, array2)[0]
    return stat

def Create_Gene_Dict(genes):
    geneDict={}
    genes.next()
    for line in genes:
        line=line.rstrip().split("\t")
        geneDict[line[3]]=[float(i) for i in line[5:]]
    return geneDict

def Create_ELS_Dict(els, column):
    elsDictA={}
    elsDictB={}
    for line in els:
        line=line.rstrip().split("\t")
        if column == "no":
            score=max(float(i) for i in line[7:-1])
        else:
            score=float(line[column])
        if line[3] not in elsDictA:
            elsDictA[line[3]]=[float(line[-1]),score]
            elsDictB[line[3]]=[float(i) for i in line[7:-1]]
        elif elsDictA[line[3]][0] < float(line[-1]):
            elsDictA[line[3]]=[float(line[-1]),score]
            elsDictB[line[3]]=[float(i) for i in line[7:-1]]
        elif elsDictA[line[3]][1] < score: #note all peak widths are 150
            elsDictA[line[3]]=[float(line[-1]),score]
            elsDictB[line[3]]=[float(i) for i in line[7:-1]]
    return elsDictB, elsDictA

def Create_Symbol_Dict(symbols):
    symbolDict={}
    for line in symbols:
        line=line.rstrip().split("\t")
        symbolDict[line[3]]=line[6]
    return symbolDict

def Create_Stat_Dict(stats):
    statDict={}
    for line in stats:
        line=line.rstrip().split("\t")
        statDict[line[0].rstrip()]=[float(line[1]),float(line[2])]
    return statDict

genes=open(sys.argv[1])
geneDict=Create_Gene_Dict(genes)
genes.close()

symbols=open(sys.argv[2])
symbolDict=Create_Symbol_Dict(symbols)
symbols.close()

column=Process_Biosample(sys.argv[6])
els=open(sys.argv[3])
elsDict, test =Create_ELS_Dict(els,column)
els.close()

stat=open(sys.argv[4])
statArray = Create_Stat_Dict(stat)
stat.close()

pairs=open(sys.argv[5])
for line in pairs:
    line=line.rstrip().split("\t")
    els=line[0]
    gene=symbolDict[line[1].rstrip()]
    if els in elsDict and gene in geneDict:
        cor=Calculate_Correlation(elsDict[els],geneDict[gene])
        if math.isnan(cor):
            cor=0
        if statArray[gene][1] != 0:
            Z=(cor-statArray[gene][0])/statArray[gene][1]
        else:
            Z=0
        p=stats.norm.sf(abs(Z))*2
        print line[2], "\t", cor, "\t", p, "\t", Z, "\t", els, "\t", line[1]
 
    else:
        print line[2], "\t", -100, "\t", 1, "\t", -100, "\t", els, "\t", line[1]
