import xgboost, joblib
from operator import add
import random, subprocess,numpy, sys, sklearn, scipy, itertools, shutil, math
        
def Run_XGB(allLabels, allFeatures, valLabels, valFeatures, output,\
                      repetitions, i, header,outputDir,version, name):
    valOutput=output+"-validation-"+str(i)+"."+version+".txt"
    fiOutput=output+"-FI-"+str(i)+"."+version+".txt"
    output=open(valOutput, "w")
    output2=open(fiOutput, "w")
    oob=[]
    acc=[]
    o=[0]*len(valLabels)
    FI=[0]*len(valFeatures[0])
    y=numpy.array(allLabels)

    weight = float(len(y[y == 0]))/float(len(y[y == 1]))
    w1 = [1]*y.shape[0]
    k=0
    for entry in allLabels:
        if entry == 1:
            w1[k] = weight
        k+=1
    w1=numpy.array(w1)

    for x in range(0,repetitions):        
        xgb = xgboost.XGBClassifier(max_depth=10, learning_rate=0.1, \
                                    n_estimators=1000, nthread=50)
        xgb.fit(numpy.array(allFeatures), numpy.array(allLabels), sample_weight=w1)
        joblib.dump(xgb, outputDir+'/'+name+'.PEP.model.'+str(x)+'.'+str(i)+'.pkl')
        M=xgb.predict_proba(numpy.array(valFeatures))
        predictions=xgb.predict(numpy.array(valFeatures))
        i=0
        correct=0
        incorrect=0
        for x in predictions:
            if x == valLabels[i]:
                correct += 1
            else:
                incorrect += 1
            i += 1
        acc.append(correct/float(correct+incorrect))
        k=0
        for entry in M:
            o[k] += entry[1]
            k += 1
        FI=[x + y for x, y in zip(FI, xgb.feature_importances_)]
    print numpy.mean(acc), weight
    j=0
    for element in FI:
        print >> output2, header[j], "\t", element/float(repetitions)
        j+=1
    print "\n"
    i=0
    for entry in o:
        print >> output, valLabels[i], "\t", entry/float(repetitions)
        i += 1
    output.close()
    output2.close()
    shutil.move(valOutput, outputDir+"/"+valOutput)
    shutil.move(fiOutput, outputDir+"/"+fiOutput)

def Run_Model(trainFeat,trainLab, outputPrefix, cvList, cvGroups, header,\
    outputDir, version):
    i=1
    for group in cvList:
        print "Running cross-validation for "+ group
        trainMatrix=[]
        testMatrix=[]
        trainY=[]
        testY=[]
        j=0
        for entry in cvGroups:
            if entry == group:
                testMatrix.append(trainFeat[j])
                testY.append(trainLab[j])
            else:
                trainMatrix.append(trainFeat[j])
                trainY.append(trainLab[j])
            j+=1
        Run_XGB(trainY, trainMatrix, testY, testMatrix, outputPrefix, 1, \
            group, header, outputDir, version, outputPrefix)
        i+=1    
    return


def Create_Gene_Dict(tss):
    tssDict={}
    geneDict={}
    for line in tss:
        line=line.rstrip().split("\t")
        tssDict[line[3]]=line[4]
        if line[4] not in geneDict:
            geneDict[line[4]]=[line[3]]
        else:
            geneDict[line[4]].append(line[3])
    return tssDict, geneDict
    
def Process_ELS_Gene_Pairs(pairs):
    pairArray=[]
    cvList=[]
    for line in pairs:
        line=line.rstrip().split("\t")
        pairArray.append([line[0],line[1],int(line[2]),line[3]])
        if line[3] not in cvList:
            cvList.append(line[3])
    return pairArray, cvList

def Process_Peak_Matrix(matrix, mode, header):
    elementDict={}
    h=matrix.next().rstrip().split("\t")[1:]
    for entry in h:
        header.append(entry+"-"+mode)
    for line in matrix:
        line=line.rstrip().split("\t")
        elementDict[line[0]]=[float(i) for i in line[1:]]
    return elementDict, header

def Create_Feature_Array(data, enhancerSignals, tssSignals, geneDict):
    labels=[]
    cvGroups=[]
    features=[]
    for pair in data:
        tssFeatures=[]
        for tss in geneDict[pair[1]]:
            if len(tssFeatures) > 0:
                tssFeatures=map(add, tssFeatures, tssSignals[tss])
            else:
                tssFeatures=tssSignals[tss]
        tssFeatures=[x / float(len(geneDict[pair[1]])) for x in tssFeatures]
        features.append(enhancerSignals[pair[0]]+tssFeatures)
        labels.append(pair[2])
        cvGroups.append(pair[3])
    return features, labels, cvGroups

header=[]
trainingPairs=open(sys.argv[1])
trainingArray, cvList=Process_ELS_Gene_Pairs(trainingPairs)
trainingPairs.close()

enhancerMatrix=open(sys.argv[2])
enhancerSignals, header=Process_Peak_Matrix(enhancerMatrix, "enhancer",header)
enhancerMatrix.close()

tssMatrix=open(sys.argv[3])
tssSignals, header=Process_Peak_Matrix(tssMatrix,"tss",header)
tssMatrix.close()

tss=open(sys.argv[4])
tssDict, geneDict=Create_Gene_Dict(tss)
tss.close()

outputPrefix=sys.argv[5]
outputDir=sys.argv[6]
version=sys.argv[7]

print "processing feature matrices..."
trainFeat, trainLab, cvGroups, =Create_Feature_Array(trainingArray, \
    enhancerSignals, tssSignals, geneDict)

print "running models..."
Run_Model(trainFeat, trainLab, outputPrefix, cvList, cvGroups, header, \
    outputDir, version)
