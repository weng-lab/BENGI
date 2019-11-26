import sys, subprocess

def Create_Bed_Files(tsv, enhancer, tss):
    bedDict={}
    bed1=open("bed1","w+")
    i=1
    tsv.next()
    for line in tsv:
        line=line.rstrip().split("\t")
	print >> bed1, line[8]+"\t"+line[9]+"\t"+line[10]+"\t"+line[1]
        i += 1
    bed1.close()
    out1=open("out1","w+")
    subprocess.call(["bedtools", "intersect", "-wo","-a", "bed1", "-b", enhancer], stdout=out1)
    out1.close()
    out1=open("out1")
    for line in out1:
        line=line.rstrip().split("\t")
        if line[3] not in bedDict:
            bedDict[line[3]]=[line[7]]
        else:
            if line[7] not in bedDict[line[3]]:
                bedDict[line[3]].append(line[7])
    out1.close()
    return bedDict

def Create_Gene_Dict(tss):
    geneDict={}
    tss=open(tss)
    for line in tss:
        line=line.rstrip().split("\t")
        master=line[6].split(".")[0]
        if master not in geneDict:
            geneDict[master]=line[6]
    tss.close()
    return geneDict
    
tsv=open(sys.argv[1])
enhancer=sys.argv[2]
tss=sys.argv[3]
bedDict = Create_Bed_Files(tsv, enhancer, tss)
geneDict=Create_Gene_Dict(tss)
tsv.close()
n=1
for gene in bedDict:
    try:
        g=geneDict[gene]
        for els in bedDict[gene]:
	    print els+"\t"+g+"\t"+"Link-"+str(n)
            n+=1
    except:
        pass
