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
    #listfiles = glob.glob("/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/inputFilesHGT/pmiMultidata/*.nwk")
    
    ##testing
    listfiles = glob.glob("/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/eclipse/*.nwk")
    #####
    for treefile in listfiles:
        ##concept name
        concept = treefile.split("/")[-1].split("+")[0]
        p = subprocess.Popen('perl ./run_hgt.pl -inputfile='+treefile,shell=True)
        os.waitpid(p.pid,0)
        
        ####move relevant files
        #move output.txt
        shutil.move("output.txt","/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/outputFilesHGT/pmiMultidata/"+concept+"+output.txt")
        ##move results.txt
        shutil.move("results.txt","/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/outputFilesHGT/pmiMultidata/"+concept+"+results.txt")
        ##move log.txt
        shutil.move("log.txt","/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/outputFilesHGT/pmiMultidata/"+concept+"+log.txt")


    #for filename in os.listdir("temp"):
    #    os.remove(os.path.join("temp",filename))
    

def hgt_computation_run(pathCT, pathBS, method):
    ##get the dictionary from the method
    overallDict = create_inputFiles.create_files(pathCT, pathBS, method)
    
    for method, conceptDict in overallDict.items():
        for concept, treefile in conceptDict.items():
            p = subprocess.Popen('perl ./run_hgt.pl -inputfile='+treefile,shell=True)
            os.waitpid(p.pid,0)
            
            ####move relevant files
            #move output.txt
            shutil.move("output.txt","/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/outputFilesHGT/"+method+"/"+concept+"+output.txt")
            ##move results.txt
            shutil.move("results.txt","/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/outputFilesHGT/"+method+"/"+concept+"+results.txt")
            ##move log.txt
            shutil.move("log.txt","/home/marisa/Dropbox/EVOLAEMP/projects/Project-Borrowing-hgt/NELex/outputFilesHGT/"+method+"/"+concept+"+log.txt")
                


if __name__ == '__main__':
    method = "pmiMultidata"
    hgt_computation_fromFiles()
    
    
    