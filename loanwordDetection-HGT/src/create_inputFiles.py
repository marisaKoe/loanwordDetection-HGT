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
+ CT rooted
+ 100 BS rooted

Char-based ML (NgramsNW)
=========================
+ LT rooted in input folder (mccTreeMB.nwk.rooted)
+ CT rooted
+ 100 BS rooted


Char-based MB
==============
+ LT rooted in input folder (mccTreeMB.nwk.rooted)
+ CT rooted
+ 100 BS rooted

Please insert path to input and output folders

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
        ##get the name of the concept
        concept = ctName.split("/")[-1].split("+")[-1].split(".")[0]

        ###comment out for mtbayes analysis

        ###if statement only needed for pmi methods
        #if "[" and "]" in concept:
        #    print concept
        #    concept = concept.replace("[","").replace("]","")
#         if "[" and "]" in concept:
#             print ctName
#             concept = concept.replace("[","").replace("]","")
#             print concept
       
        ##read the concpet tree in dendropy
        conTree = Tree.get(path=ctName, schema="newick",rooting="default-rooted")
        ##get list of leaves for the concept tree
        nodes_list_con = [n.taxon.label for n in conTree.leaf_node_iter()]
        ##if the lists are equal, no pruning is necessary
        if len(nodes_list_exp) == len(nodes_list_con):
            ##get the path for the language tree
            ##please insert path to folder
            pathConceptExTree = path = "path-to-folder"+method+"Input/"+concept+"+hgt.nwk"
            ##write the language tree in a file
            expertTree.write(path=pathConceptExTree, schema="newick",suppress_rooting=True)
        ##otherwise, prune language tree according to the leaves in the concept tree
        else:
            ##clode the expert tree
            conceptExTree = Tree.clone(expertTree, depth=2)
            ##prune the language tree with the node list of the concept tree
            conceptExTree.retain_taxa_with_labels(nodes_list_con)
            ##get the path for the language tree
            ##please insert path to folder
            pathConceptExTree = path = "path-to-folder"+method+"Input/"+concept+"+hgt.nwk"
            ##write the language tree in a file
            conceptExTree.write(path=pathConceptExTree, schema="newick",suppress_rooting=True)
         
        ###if statement only needed for pmi methods
        #if "[" and "]" in concept:
        #    concept = concept.replace("[","").replace("]","")
        #print "hello concept", concept
        for bsName in BSFiles:
            #concept = concept.replace("[","").replace("]","")
            if concept in bsName:
                count += 1
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
        ##please insert path to folder
        path = "path-to-folder"+method+"Input/"+concept+"+hgt.nwk"
        #overallDict[method][concept]=path
        with open(path,"a") as fout:
            fout.write(ct)
            for line in bs:
                fout.write(line)
    
    return overallDict
    

        
        
    
    





if __name__ == '__main__':
    ##please insert path to files
    pathCT = "path-to-concept-tree-files"
    pathBS = "path-to-bootstrapReplicates-concept-trees"
    method = "name of the concept tree reconstruction method"
    create_files(pathCT, pathBS,method)
    
    
    
    
    
    