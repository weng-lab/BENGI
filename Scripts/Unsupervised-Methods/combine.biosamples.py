import sys, scipy, numpy
from scipy import stats

def Process_Data(inputData):
    dataDict={}
    inputData=open(inputData)
    for line in inputData:
        line=line.rstrip().split("\t")
        if line[1] not in dataDict:
            dataDict[line[1]]=[[] for i in range(32)]
            dataDict[line[1]][int(line[0])-1].append(float(line[2]))
        else:
            dataDict[line[1]][int(line[0])-1].append(float(line[2]))
    finalDict={}
    inputData.close()
    for entry in dataDict:
        finalDict[entry]=[]
        for i in dataDict[entry]:
            finalDict[entry].append(numpy.mean(i))
            #finalDict[entry].append(numpy.sum(i))
    return finalDict

dataDict=Process_Data(sys.argv[1])

for entry in dataDict:
    print entry+"\t"+"\t".join([str(i) for i in dataDict[entry]])
