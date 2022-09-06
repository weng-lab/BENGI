import sys


tssDict={}
for line in open(sys.argv[1]):
        line=line.rstrip().split("\t")
        if line[6] in tssDict:
                tssDict[line[6]].append(int(line[1]))
        else:
                tssDict[line[6]]=[int(line[1])]

enhancerDict={}
for line in open(sys.argv[2]):
        line=line.rstrip().split("\t")
        enhancerDict[line[3]]=[int(line[1]),int(line[2])]

for line in open(sys.argv[3]):
        line=line.rstrip().split("\t")
        m=1000000000000
        for x in tssDict[line[1]]:
                a=min([abs(enhancerDict[line[0].rstrip()][0]-x),abs(enhancerDict[line[0].rstrip()][1]-x)])
                if a < m:
                        m=a
        print line[0]+"\t"+line[1]+"\t"+str(m)
