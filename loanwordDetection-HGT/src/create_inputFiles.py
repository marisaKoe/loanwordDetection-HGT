'''
Created on 08.08.2019

@author: marisa

create the input files for hgt algorithm from Boc et al
input file:
+ LT rooted
+ CT rooted
+ 100 BS replicated rooted

Distance-based Method (PMI_MultipleData)
==========================================
+ LT rooted in input folder (mccTreeMB.nwk.rooted)
+ CT rooted: "/home/marisakoe/Dropbox/EVOLAEMP/projects/Project-ConceptTrees-DistanceMethods/NELex/PMI_based_methods/PMI_multipleData_rootedTrees/"
+ 100 BS rooted: "/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/inputTrees/"+method+"/*.nwk" method = pmiMultidata

Char-based ML (NgramsNW)
=========================
+ LT rooted in input folder (mccTreeMB.nwk.rooted)



Char-based MB
==============
+ LT rooted in input folder (mccTreeMB.nwk.rooted)


################    TODO    #################
if all trees are ready:
create a dictionary with key = method and value=list of files
go through the dict and do analysis for each method

+ check method since it is not clear if the concepts for each method contain []
'''

import glob, collections
from collections import defaultdict

def create_files(pathCT, pathBS, method):
    '''
    create the input files for the hgt algorithm
    :param pathCT: path to the concept tree
    :param pathBS: path to the 100 BS replicates
    '''
    ##read language tree
    with open("input/mccTreeMB.nwk.rooted","r") as flt:
        ##file contains only one line
        lt = flt.readline()
    
    CTFiles = glob.glob(pathCT+"*.nwk.rooted")
    BSFiles = glob.glob(pathBS+"*.rooted")
    ##fill the dictionary with the file names
    fileDict = defaultdict(list)
    for ctName in CTFiles:
        concept = ctName.split("/")[-1].split(".")[0]
        if "[" and "]" in concept:
            concept = concept.replace("[","").replace("]","")
        #print concept
        for bsName in BSFiles:
            if concept in bsName:
                fileDict[concept] = [ctName,bsName]
                
    ##read the files for each concepts and glue them together into one         
    for concept, fileList in fileDict.items():
        ##open concept tree
        with open(fileList[0],"r") as fct:
            ##concept tree contains one line
            ct = fct.readline()
        ##open bs samples (100 trees)
        with open(fileList[1],"r") as fbs:
            bs = fbs.readlines()
            
        ##write files into folder
        with open("/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/inputFilesHGT/"+method+"/"+concept+"+hgt.nwk","w") as fout:
            fout.write(lt+ct)
            for line in bs:
                fout.write(line)
    

        
        
    
    





if __name__ == '__main__':
    method = "pmiMultidata"
    pathCT = "/home/marisa/Dropbox/EVOLAEMP/projects/Project-ConceptTrees-DistanceMethods/NELex/PMI_based_methods/PMI_multipleData_rootedTrees/"
    pathBS = "/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/rootingMAD/NELex/"+method+"/"
    create_files(pathCT, pathBS,method)
    
    
    
    
    
    