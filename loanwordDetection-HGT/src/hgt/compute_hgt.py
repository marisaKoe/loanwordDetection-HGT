'''
Created on 09.08.2019

@author: marisa

hgt are computed using the hgt algorithm from Boc et al.

the algorithm is an executable and a pearl script

+ read the input files
+ for each file, call the algorithm
    - perl run_hgt.pl -inputfile=inputfilename [-mode=multicheck -criterion=bd -bootstrap=yes]
    
+ move files, which are need for further analysis -> rename them
    - output.txt
    - results.txt
'''
import glob, subprocess, os, shutil
import create_inputFiles

def hgt_computation_fromFiles():
    
    ##get all files containing the trees for the computation for each concept
    ##glob reads all files contained in one folder and stores it in a list of files
    listfiles = glob.glob("path to folder containing concept tree files")
    
  
    for treefile in listfiles:
        ##concept name
        concept = treefile.split("/")[-1].split("+")[0]
        run_hgt(concept, treefile)

    

def hgt_computation_run(pathCT, pathBS, method):
    ##get the dictionary from the method
    overallDict = create_inputFiles.create_files(pathCT, pathBS, method)
    
    for method, conceptDict in overallDict.items():
        for concept, treefile in conceptDict.items():
            run_hgt(concept, treefile)
                

    
def run_hgt(concept,treefile):
        #p = subprocess.Popen('exec perl ./run_hgt.pl -inputfile='+treefile,stdout=subprocess.PIPE,shell=True)
        ##runs the hgt script! Please make sure you downladed the program and ajust the command for your purpose
        p = subprocess.Popen('perl ./run_hgt.pl -inputfile='+treefile+' -bootstrap=yes',shell=True)
        os.waitpid(p.pid,0)
        #p.kill()
        ####move relevant files - please insert your preferred path to the folder you would like to store the files
        ##move output.txt
        shutil.move("output.txt","path-to-folder"+concept+"+output.txt")
        ##move results.txt
        shutil.move("results.txt","path-to-folder"+concept+"+results.txt")
        ##move log.txt
        shutil.move("log.txt","path-to-folder"+concept+"+log.txt")

if __name__ == '__main__':
    method = "pmiMultidata"
    hgt_computation_fromFiles()
    
    
    