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

import glob, collections, dendropy
from collections import defaultdict
from dendropy import Tree

def create_files(pathCT, pathBS, method):
    '''
    create the input files for the hgt algorithm
    :param pathCT: path to the concept tree
    :param pathBS: path to the 100 BS replicates
    '''
    ##read language tree
    #with open("input/mccTreeMB.nwk.rooted","r") as flt:
        ##file contains only one line
        #lt = flt.readline()
    ##read the expert tree in dendropy
    expertTree = Tree.get(path="input/mccTreeMB.nwk.rooted", schema="newick",rooting="default-rooted")
    nodes_list_exp = [n.taxon.label for n in expertTree.leaf_node_iter()]
    
    CTFiles = glob.glob(pathCT+"*.rooted")
    BSFiles = glob.glob(pathBS+"*.rooted")
    #print CTFiles
    ##fill the dictionary with the file names
    fileDict = defaultdict(list)
    overallDict = defaultdict(dict)
    count = 0
    for ctName in CTFiles:
        print ctName
        ##get the name of the concept
        concept = ctName.split("/")[-1].split("+")[-1].split(".")[0]
        print "first time", concept
        ###if statement only needed for pmi methods
        if "[" and "]" in concept:
            concept = concept.replace("[","").replace("]","")
        print "second time", concept
        ##read the concpet tree in dendropy
        conTree = Tree.get(path=ctName, schema="newick",rooting="default-rooted")
        ##get list of leaves for the concept tree
        nodes_list_con = [n.taxon.label for n in conTree.leaf_node_iter()]
        print len(nodes_list_con)
        ##if the lists are equal, no pruning is necessary
        if len(nodes_list_exp) == len(nodes_list_con):
            ##get the path for the language tree
            pathConceptExTree = path = "/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/"+method+"Input/"+concept+"+hgt.nwk"
            ##write the language tree in a file
            expertTree.write(path=pathConceptExTree, schema="newick",suppress_rooting=True)
        ##otherwise, prune language tree according to the leaves in the concept tree
        else:
            ##clode the expert tree
            conceptExTree = Tree.clone(expertTree, depth=2)
            ##prune the language tree with the node list of the concept tree
            conceptExTree.retain_taxa_with_labels(nodes_list_con)
            ##get the path for the language tree
            pathConceptExTree = path = "/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/"+method+"Input/"+concept+"+hgt.nwk"
            ##write the language tree in a file
            conceptExTree.write(path=pathConceptExTree, schema="newick",suppress_rooting=True)
        
        ###if statement only needed for pmi methods
        #if "[" and "]" in concept:
        #    concept = concept.replace("[","").replace("]","")
        print "hello concept", concept
        for bsName in BSFiles:
            #print bsName
            
            if concept in bsName:
                print "im in the string", concept
                count += 1
                fileDict[concept] = [ctName,bsName]
    #print count
    #print len(fileDict)
    ##read the files for each concepts and glue them together into one   
          
    for concept, fileList in fileDict.items():
        print concept, fileList
        ##open concept tree
        with open(fileList[0],"r") as fct:
            ##concept tree contains one line
            ct = fct.readline()
        
        ##open bs samples (100 trees)
        with open(fileList[1],"r") as fbs:
            bs = fbs.readlines()
          
        ##write files into folder
        path = "/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/"+method+"Input/"+concept+"+hgt.nwk"
        #overallDict[method][concept]=path
        with open(path,"a") as fout:
            fout.write(ct)
            for line in bs:
                fout.write(line)
    
    return overallDict
    

        
        
    
    





if __name__ == '__main__':
    ###pmi multipleData
    #method = "pmiMultidata"
    #pathCT = "/home/marisakoe/Dropbox/EVOLAEMP/projects/Project-ConceptTrees-DistanceMethods/NELex/PMI_based_methods/PMI_multipleData_rootedTrees/"
    #pathBS = "/home/marisakoe/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/rootingMAD/NELex/"+method+"/"
    #create_files(pathCT, pathBS,method)
    ##ml ngramsNW
    #method = "ML_ngramsNW"
    #pathCT = "/home/marisakoe/Dropbox/EVOLAEMP/projects/Project-ConceptTrees-CharacterBased/NELex/ML_iqtree/NgramsNW/iqTrees/"
    #pathBS = "/home/marisakoe/Dropbox/EVOLAEMP/projects/Project-ConceptTrees-CharacterBased/NELex/ML_iqtree/NgramsNW/bootstrapReplicates/"
    #create_files(pathCT, pathBS,method)
    ###mb NW
    method= "MB_NW"
    pathCT = "/home/marisa/Dropbox/EVOLAEMP/projects/Project-ConceptTrees-CharacterBased/NELex/MrBayes_Trees/mccTrees/"
    pathBS = "/home/marisa/Dropbox/EVOLAEMP/projects/Project-MADRooting/NELex/MB_NW/"
    create_files(pathCT, pathBS,method)
    
    
    
    
    
    