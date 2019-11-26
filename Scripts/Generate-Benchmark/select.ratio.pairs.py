import sys, random

def Create_ccRE_Dict(pairs, ccreDict):
    for line in pairs:
        line=line.rstrip().split("\t")
        position=int(line[2])
        if line[0] not in ccreDict:
            ccreDict[line[0]]=[[],[]]
        ccreDict[line[0]][position].append(line[1])
    return ccreDict

def Process_ccRE_Dict(ccreDict):
    skip=0
    include=0
    output=open("skip.txt","w+")
    for els in ccreDict:
        if len(ccreDict[els][0]) >= 4:
            pos = random.sample(ccreDict[els][1],1)
            neg = random.sample(ccreDict[els][0],4)
            for entry in pos:
                print els.rstrip()+"\t"+entry.rstrip()+"\t"+"1"
            for entry in neg:
                print els.rstrip()+"\t"+entry.rstrip()+"\t"+"0"
            include += 1
        else:
            skip+=1
    print >> output, include, "\t", skip
    output.close()
    

ccreDict={}
pairs=open(sys.argv[1])
ccreDict=Create_ccRE_Dict(pairs, ccreDict)
pairs.close()

Process_ccRE_Dict(ccreDict)


