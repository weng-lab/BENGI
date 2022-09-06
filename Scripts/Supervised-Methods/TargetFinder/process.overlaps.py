
import sys

def Create_Element_Dict(elements):
    elementDict={}
    for line in elements:
        line=line.rstrip().split("\t")
        elementDict[line[3]]=[float(int(line[2])-int(line[1])),0]
    return elementDict

def Process_Overlaps(overlaps, elementDict, mode):
    for line in overlaps:
        line=line.rstrip().split("\t")
        if mode == "peaks":
            elementDict[line[3]][1]+=float(line[11])
        elif mode == "cage":
            elementDict[line[3]][1]+=float(line[9])
        elif mode == "rrbs":
            elementDict[line[3]][1]+=float(line[-1])
    for entry in elementDict:
        if elementDict[entry][0] > 0:
            print entry+"\t"+str(elementDict[entry][1]/elementDict[entry][0])
        else:
	    print entry+"\t"+"0"

mode=sys.argv[3]
    
elements=open(sys.argv[1])
elementDict=Create_Element_Dict(elements)
elements.close()

overlaps=open(sys.argv[2])
Process_Overlaps(overlaps,elementDict,mode)
overlaps.close()



