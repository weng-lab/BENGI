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
        enhancerDict[line[3]]=[int(line[1]),int(line[2])]
    enhancers.close()
    return enhancerDict


    
tss=sys.argv[1]
tssDict=Create_TSS_Dict(tss)

enhancers=sys.argv[2]
enhancerDict=Create_Enhancer_Dict(enhancers)

links=open(sys.argv[3])
output=open(sys.argv[4], "w+")
distanceArray=[]

for line in links:
    line=line.rstrip().split("\t")
    m=1000000000000
    for x in tssDict[line[1]]:
        a=min([abs(enhancerDict[line[0].rstrip()][0]-x),abs(enhancerDict[line[0].rstrip()][1]-x)])
        if a < m:
            m=a
    print >> output, line[0]+"\t"+line[1]+"\t"+str(m)
    distanceArray.append(m)

links.close()
output.close()

print np.percentile(distanceArray,95)




