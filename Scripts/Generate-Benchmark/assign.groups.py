import sys

def Determine_Groups(chromDict):
    chromArray=[]
    groupDict={}
    for key, value in sorted(chromDict.iteritems(), key=lambda (k,v): (v,k)):
        chromArray.append(key)
    for i in range(0,11):
        groupDict[chromArray[i]]="cv-"+str(i)
        groupDict[chromArray[-2-i]]="cv-"+str(i)
    groupDict[chromArray[-1]]="cv-11"
    return groupDict

def Create_Chrom_Dict(enhancers):
    chromDict={}
    enhancerDict={}
    for line in enhancers:
        line=line.rstrip().split("\t")
        line[0]=line[0].rstrip()
        if line[0] not in chromDict:
            chromDict[line[0]]=1
        else:
            chromDict[line[0]]+=1
        if line[3].rstrip() not in enhancerDict:
            enhancerDict[line[3].rstrip()]=line[0]
    return chromDict, enhancerDict

enhancers=open(sys.argv[1])
chromDict, enhancerDict = Create_Chrom_Dict(enhancers)
enhancers.close()
groupDict=Determine_Groups(chromDict)

pairs=open(sys.argv[2])


for line in pairs:
    line=line.rstrip()
    x=line.split("\t")
    print line, "\t", groupDict[enhancerDict[x[0].rstrip()]]
    
pairs.close()
    
