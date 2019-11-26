import sys, subprocess

def Create_Bed_Files(tsv, enhancer, tss):
    bedDict={}
    bed1=open("bed1","w+")
    bed2=open("bed2","w+")
    i=1
    #tsv.next()
    for line in tsv:
        line=line.rstrip().split("\t")
	if line[0] == line[3]:
            print >> bed1, line[0]+"\t"+line[1]+"\t"+line[2]+"\t"+"Link-"+str(i)
            print >> bed2, line[3]+"\t"+line[4]+"\t"+line[5]+"\t"+"Link-"+str(i)
        i += 1
    bed1.close()
    bed2.close()
    out1=open("out1","w+")
    out2=open("out2","w+")
    subprocess.call(["bedtools", "intersect", "-wo","-a", "bed1", "-b", enhancer], stdout=out1)
    subprocess.call(["bedtools", "intersect", "-wo","-a", "bed1", "-b", tss], stdout=out2)
    out1.close()
    out2.close()
    out1=open("out1")
    for line in out1:
        line=line.rstrip().split("\t")
        if line[3] not in bedDict:
            bedDict[line[3]]=[[line[7]],[],[],[]]
        else:
            if line[7] not in bedDict[line[3]][0]:
                bedDict[line[3]][0].append(line[7])
    out1.close()
    out2=open("out2")
    for line in out2:
        line=line.rstrip().split("\t")
        if line[3] not in bedDict:
            bedDict[line[3]]=[[],[line[10]],[],[]]
        else:
            if line[10] not in bedDict[line[3]][1]:
                bedDict[line[3]][1].append(line[10])
    out1=open("out1","w+")
    out2=open("out2","w+")
    subprocess.call(["bedtools", "intersect", "-wo","-a", "bed2", "-b", enhancer], stdout=out1)
    subprocess.call(["bedtools", "intersect", "-wo","-a", "bed2", "-b", tss], stdout=out2)
    out1.close()
    out2.close()
    out1=open("out1")
    for line in out1:
        line=line.rstrip().split("\t")
        if line[3] not in bedDict:
            bedDict[line[3]]=[[],[],[line[7]],[]]
        else:
            if line[7] not in bedDict[line[3]][2]:
                bedDict[line[3]][2].append(line[7])
    out1.close()
    out2=open("out2")
    for line in out2:
        line=line.rstrip().split("\t")
        if line[3] not in bedDict:
            bedDict[line[3]]=[[],[],[],[line[10]]]
        else:
            if line[10] not in bedDict[line[3]][3]:
                bedDict[line[3]][3].append(line[10])
    return bedDict
    
    
tsv=open(sys.argv[1])
enhancer=sys.argv[2]
tss=sys.argv[3]
bl=open(sys.argv[4], "w+")
status=sys.argv[5]

bedDict = Create_Bed_Files(tsv, enhancer, tss)
n=1
for entry in bedDict:
    x=bedDict[entry]
    #print entry, "\t", bedDict[entry]
    if status == "yes":
        if len(x[0]) > 0 and len(x[1]) == 0 and len(x[3]) == 1:
            for i in x[0]:
                print i+"\t"+x[3][0]+"\t"+entry
	        n+=1
        elif len(x[1]) == 1 and len(x[2]) > 0 and len(x[3]) == 0:
            for i in x[2]:
                print i+"\t"+x[1][0]+"\t"+entry
	        n+=1
        else:
            if len(x[0]) > 0 and len(x[3]) > 0:
   	        for i in x[0]:
	            for j in x[3]:
		        print >> bl , i+"\t"+j+"\t"+entry
		        n+=1
            if len(x[1]) > 0 and len(x[2]) > 0:
	        for i in x[2]:
	            for j in x[1]:
		        print >> bl , i+"\t"+j+"\t"+entry
		        n+=1
    else:
        if len(x[0]) > 0 and len(x[3]) > 0:
            for i in x[0]:
                for j in x[3]:
                    print i+"\t"+j+"\t"+"Link-"+str(n)
                    n+=1
        if len(x[1]) > 0 and len(x[2]) > 0:
            for i in x[2]:
                for j in x[1]:
                    print i+"\t"+j+"\t"+"Link-"+str(n)
                    n+=1
    
tsv.close()
bl.close() 
