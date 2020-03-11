import sys, numpy as np

def Create_TSS_Dict(tss):
    tss=open(tss)
    tssDict={}
    for line in tss:
        line=line.rstrip().split("\t")
        if line[6] in tssDict:
            tssDict[line[6]].append(int(line[1]))
        else:
            tssDict[line[6]]=[int(line[1])]
    tss.close()
    return tssDict

def Create_Enhancer_Dict(enhancers):
    enhancers=open(enhancers)
    enhancerDict={}
    for line in enhancers:
        line=line.rstrip().split("\t")
        enhancerDict[line[4]]=[int(line[1]),int(line[2])]
    enhancers.close()
    return enhancerDict

def Create_Expression_Dict(expression):
    expressionDict={}
    expression=open(expression)
    for line in expression:
        line=line.rstrip().split("\t")
        expressionDict[line[0]]=float(line[1])
    expression.close()
    return expressionDict


    
tss=sys.argv[1]
tssDict=Create_TSS_Dict(tss)

enhancers=sys.argv[2]
enhancerDict=Create_Enhancer_Dict(enhancers)

expression=sys.argv[4]
print expression
expressionDict=Create_Expression_Dict(expression)

links=open(sys.argv[3])
output=open(sys.argv[6], "w+")
distanceArray=[]

cutoff=float(sys.argv[5])

for line in links:
    line=line.rstrip().split("\t")
    m=1000000000000
    for x in tssDict[line[1]]:
        a=min([abs(enhancerDict[line[0].rstrip()][0]-x),abs(enhancerDict[line[0].rstrip()][1]-x)])
        if a < m:
            m=a
    if expressionDict[line[1]] > cutoff: 
        print >> output, line[2]+"\t"+str(1/float(m))
    else:
	print >> output, line[2]+"\t"+"0"
    distanceArray.append(m)

links.close()
output.close()





