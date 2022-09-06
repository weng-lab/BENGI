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
        enhancerDict[line[3]]=[int(line[1]),int(line[2]), line[0]]

for line in open(sys.argv[3]):
        line=line.rstrip().split("\t")
        m=1000000000000
	t=""
        for x in tssDict[line[1]]:
                a=min([abs(enhancerDict[line[0].rstrip()][0]-x),abs(enhancerDict[line[0].rstrip()][1]-x)])
		
                if a < m:
                        m=a
			t=x
	if a <= 500:
	    start=enhancerDict[line[0].rstrip()][0]
	    stop=enhancerDict[line[0].rstrip()][0]	    
	elif t < enhancerDict[line[0].rstrip()][0]:
	    start=t+500
	    stop=enhancerDict[line[0].rstrip()][0]
	elif t > enhancerDict[line[0].rstrip()][0]:
	    start=enhancerDict[line[0].rstrip()][1]
	    stop=t-500
	if start <= stop:
	    print enhancerDict[line[0].rstrip()][2]+"\t"+str(start)+"\t"+str(stop)+"\t"+\
	    line[0].rstrip()+"-"+line[1].rstrip()+"\t"+str(m)
	else:
	    print enhancerDict[line[0].rstrip()][2]+"\t"+str(enhancerDict[line[0].rstrip()][0])+"\t"+ \
	    str(enhancerDict[line[0].rstrip()][0])+"\t"+line[0].rstrip()+"-"+line[1].rstrip()+"\t"+str(m)
