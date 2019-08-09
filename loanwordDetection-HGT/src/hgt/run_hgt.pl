#!/usr/bin/perl

#use strict;
#use warnings;

#======================================================
#= VERIFICATION DES ARGUMENTS DE LA LIGNE DE COMMANDE
#======================================================
if( scalar @ARGV < 0){
    print "\nErreur\nusage : $0";
    exit 0;
}

my $cmd = "./hgt ";
my $inputfile = "";
my $outputfile="output.txt";
my $bootstrap = "no";
my $path = ""; #"./";
my $viewtree="no";
my @tmp_tab;
my @tmp_tab_init;
my %hgt;
my $ligne;
my $nbLines = 5;
my %hgt_number_tab;
my %hgt_description_tab;
my %hgt_compteur_tab;
my %hgt_criterion_tab;
my %hgt_nbHGT_tab;
my @hgt_pos;
my @hgt_pos2;
my $mode;
my $total_hgt;
my $total_trivial;
my $val_retour=0;   #= nombre de hgt trouve
my @hgt_tab;
my $rand_bootstrap = 0;
my  $speciesroot = "midpoint";
my  $generoot = "midpoint";

#==== READ PARAMETERS ====
foreach my $elt (@ARGV){
  $cmd .= $elt . " ";
  if($elt =~ "bootstrap"){
    @tmp_tab = split("=",$elt);
    $bootstrap = $tmp_tab[1];
    chomp($bootstrap);
    #print STDOUT "$bootstrap";
  }
  if($elt =~ "speciesroot"){
    @tmp_tab = split("=",$elt);
    $speciesroot = $tmp_tab[1];
    chomp($speciesroot);
  }
  if($elt =~ "generoot"){
    @tmp_tab = split("=",$elt);
    $generoot = $tmp_tab[1];
    chomp($generoot);
  }
  if($elt =~ "inputfile"){
    @tmp_tab = split("=",$elt);
    $inputfile = $tmp_tab[1];
  }
  if($elt =~ "path"){
    @tmp_tab = split("=",$elt);
    $path = $tmp_tab[1];
  }
  if($elt =~ "viewtree"){
    @tmp_tab = split("=",$elt);
    $viewtree = $tmp_tab[1];
  }
  if($elt =~ "outputfile"){
    @tmp_tab = split("=",$elt);
    $outputfile = $tmp_tab[1];
  }
  if($elt =~ "help"){
	print_description();
	print_help();
	exit;
  }
}

$inputfile    = "$path" . "$inputfile";
$outputfile = "$path" . "$outputfile";
#$cmd          = "./" . $cmd;
my $results   = "$path" . "results.txt";
my $tmp_input = "$path" . "tmp_input.txt";
my $input_no_space    = "$path" . "input_no_space.txt";
my $return_file = "$path" . "return.txt";
my $log_file = "$path" . "log.txt";
my $output_tmp;
my $outputWeb = "$path" . "outputWeb.txt";
my $generootfile = "$path" . "geneRootLeaves.txt";
my $speciesrootfile = "$path" . "speciesRootLeaves.txt";
my $generootfiletmp = "$path" . "geneRootTmp.txt";
my $speciesrootfiletmp = "$path" . "speciesRootTmp.txt";
my $inputfileformated = "$path" . "inputfileformated.txt";

 #===== PRINT HEADER =====
  print_title();

  
#= linux like  
#`rm -rf $results $outputfile $log_file $return_file $outputWeb`;

#= windows
`del $results $outputfile $log_file $return_file $outputWeb`;

#===== CHECKING FILES =====
if( $inputfile eq ""){
	print STDOUT "\n\nRUN_HGT : There is no input file";
	exit -1;
}
if( ! -e $inputfile){
	print STDOUT "\n\nRUN_HGT : $inputfile doesn't exist";
	exit -1;
}

if( ($speciesroot eq "file") && ( ! -e $speciesrootfile) ){
	print STDOUT "\n\nRUN_HGT : $speciesrootfile doesn't exist";
	exit -1;
}

if( ($generoot eq "file") && ( ! -e $generootfile) ){
	print STDOUT "\n\nRUN_HGT : $generootfile doesn't exist";
	exit -1;
}
   
  #=== LECTURE DE L'ARBRE D'ESPECES ===
  open(IN,"$inputfile") ||  die "Cannot open $inputfile";
  open(OUT,">$inputfileformated") ||  die "Cannot open $inputfileformated";
  while($ligne = <IN>){
	chomp($ligne);
	$ligne =~ s/;/;\n/g;
	if($ligne ne ""){
		print OUT $ligne;
	}
  }
  close(IN);
  close(OUT); 
  open(IN,"$inputfileformated") ||  die "Cannot open $inputfileformated";
  my @trees_tab = <IN>;
  close(IN);
  
  #===========================================================================
  #======================== EXECUTION DU PROGRAMME ===========================
  #===========================================================================
  $cmd .= "-inputfile=$tmp_input -outputfile=$outputfile"; # > $log_file";
  
  my $nbTrees = 0 ; # scalar @trees_tab - 1;
  if($bootstrap eq "yes"){
	#$nbTrees -= 1; 
  }
  
  #== The program need at least 2 trees
  if((scalar @trees_tab < 2)){
    exit_program(-1,$return_file,"PERL : nombre d'arbres invalide");
  }
  
  print_minidoc(); 
  
  for (my $i=0;(($i< scalar @trees_tab) && $trees_tab[$i] =~ ";");){
    #print STDOUT "\n==== $i\n";
    open(IN,">$tmp_input") ||  die "Cannot open $tmp_input";
	
    #================================================================================
	#= In the bootstrap case, we need to change the speciesroot and generoot option
	#= for "file" from the first replicate.
	#================================================================================
	if($bootstrap eq "yes"){
		if($i == 0){ 
			print IN $trees_tab[0] . $trees_tab[1];
			$i=2;
			$cmd .= " -randbootstrap=$rand_bootstrap";
        }
		else{
			print IN $trees_tab[0] . $trees_tab[$i++];
		}
		#print STDOUT $trees_tab[0] . $trees_tab[$i];
  		if($i > 2){
			if($cmd !~ /printWeb=no/){
				$cmd .= " -printWeb=no ";
			}
			
		}
		if($nbTrees == 1){
			$cmd =~ s/-generoot=[a-z][a-z]* //;
			$cmd =~ s/-speciesroot=[a-z][a-z]* //;
			$cmd .= " -generoot=file -speciesroot=file";
			#print STDOUT "PERL : 1 : nbTress=$nbTrees";
			
			#= linux
			#`cp $generootfile $generootfiletmp`;
			#`cp $speciesrootfile $speciesrootfiletmp`;			
			
			#= windows
			`copy $generootfile $generootfiletmp`;
			`copy $speciesrootfile $speciesrootfiletmp`;
		}
		if($nbTrees > 1){
			#== linux like
			#`cp $generootfiletmp $generootfile`;
			#`cp $speciesrootfiletmp $speciesrootfile`;
			
			#== windows
			`copy $generootfiletmp $generootfile`;
			`copy $speciesrootfiletmp $speciesrootfile`;
		}
		
		
		
		if($rand_bootstrap == 1){
			$rand_bootstrap = 0;
			$cmd =~ s/randbootstrap=1/randbootstrap=0/;
		}
		else{
			$rand_bootstrap = 1;
			$cmd =~ s/randbootstrap=0/randbootstrap=1/;
		}
    }
    else{
        print IN $trees_tab[$i++] . $trees_tab[$i++];
    }
    close(IN);
    
	print STDOUT "\nComputation " . ++$nbTrees . " in progress...";
	
    execute_hgt("$cmd >> $log_file");
	if( ! -e $results){
	  print STDOUT "\n\nRUN_HGT : An error has occured during computation. Check the log file ($log_file) for more details ! ";
	  exit -1;
    }
	print STDOUT "formatting results...";
	
    if((($i == 2) && ($viewtree eq "yes")) || (($i == 1) && ($viewtree eq "yes"))){
       exit_program(0,$return_file,"RUN_HGT : We just want to see the input tress");
    }
    
  #===========================================================================
  #========================= LECTURE DES RESULTATS ===========================
  #===========================================================================
    open(IN,"$results") ||  die "\nCannot open $results ! !!";
    @hgt_tab = <IN>;
    close(IN); 
 	
    exit_program(-1,$return_file,"RUN_HGT : result file empty") if(scalar @hgt_tab == 0);  
     
    $mode = $hgt_tab[1];
    chomp($mode);
    
    if(($i == 2) || ($bootstrap eq "no")){
		
		print STDOUT "done";
        my $nbHGT=0;
        my $nbHGT2=0;
        for(my $j=2;$j<= scalar @hgt_tab;){
            if($hgt_tab[$j] =~ /^[0-9]/){
                my $cpt = read_line($hgt_tab[$j++]);
                for(my $k=0;$k<$cpt;$k++){ 
                    my $hgt_number = read_line($hgt_tab[$j++]);
                    my $source_list = read_line($hgt_tab[$j++]);
                    my $dest_list = read_line($hgt_tab[$j++]);
					my $transfer_description2 = read_line($hgt_tab[$j++]);
					my $transfer_description = "From subtree ($source_list) to subtree ($dest_list)"; 
					
                    my $criterion_list = read_line($hgt_tab[$j++]);
                    
                    $hgt_number_tab{"$source_list -> $dest_list"}      = $hgt_number;
                    $hgt_description_tab{"$source_list -> $dest_list"} = $transfer_description;
                    $hgt_compteur_tab{"$source_list -> $dest_list"}    = 1;
                    $hgt_criterion_tab{"$source_list -> $dest_list"}   = $criterion_list;
                    $hgt_nbHGT_tab{"$source_list -> $dest_list"}       = $cpt;
                    $hgt_pos[$nbHGT++] = "$source_list -> $dest_list";
                }
                if($mode eq 'mode=multicheck'){
                    $hgt_pos2[$nbHGT2++] = read_line($hgt_tab[$j++]);
                    
                }
            }
            else{
                @tmp_tab_init = split(",",$hgt_tab[0]);
                @tmp_tab = split(" ",$hgt_tab[$j]);
                $total_hgt = $tmp_tab[1];
                $total_trivial = $tmp_tab[2];
                if($bootstrap eq "no"){
    				open(OUT,">>$outputfile") || die "Cannot open $outputfile";
                    if($total_hgt > 0){
                        print_result();
                    }
                    else{
                        print OUT " : no HGTs have been found !";
                    }
                   
                    close(OUT);
                    
                    exit_program($val_retour,$return_file,"PERL : pas de bootstrap, on traite un seul input");
                    %hgt_number_tab=();
                    %hgt_description_tab=();
                    %hgt_compteur_tab=();
                    %hgt_criterion_tab=();
                    %hgt_nbHGT_tab=();
                    @hgt_pos=();
                    @hgt_pos2=();
                } 
                $j = (scalar @hgt_tab) + 1;
            }
        } 
    }
    
    if(($bootstrap eq "yes") && ($i > 2)){
		print STDOUT "done";
        my $nbHGT=0;
        my $nbHGT2=0;
        for(my $j=2;$j<= scalar @hgt_tab;){
            if($hgt_tab[$j] =~ /^[0-9]/){
                my $cpt = read_line($hgt_tab[$j++]);
                for(my $k=0;$k<$cpt;$k++){ 
					my $hgt_number = read_line($hgt_tab[$j++]);
                    my $source_list = read_line($hgt_tab[$j++]);
                    my $dest_list = read_line($hgt_tab[$j++]);
					my $transfer_description2 = read_line($hgt_tab[$j++]);
					my $transfer_description = "From subtree ($source_list) to subtree ($dest_list)"; 
					
                    my $criterion_list = read_line($hgt_tab[$j++]);
                    
                    if(exists $hgt_compteur_tab{"$source_list -> $dest_list"}){
                        $hgt_compteur_tab{"$source_list -> $dest_list"}   += 1;
                    }
                }
                if($mode eq 'mode=multicheck'){
                    $j++;
                }
            }
            else{
                $j = (scalar @hgt_tab) + 1;
            }
        } 
    }
} 

if($bootstrap eq "yes"){
	open(OUT,">>$outputfile") || die "Cannot open $outputfile";
	print_result();
	close(OUT);
}

exit_program($val_retour,$return_file,"PERL : fin normale du programme");
              
#===============================================================================
#=============================== FUNCTIONS =====================================
#===============================================================================

sub read_line{
  my ($line) = @_;
  chomp($line);
  return $line;
}

sub exit_program{
  my($val,$file,$message) = @_;
  open(RET,">$file") || die "Cannot open $file";
  print RET $val;
  close(RET);
  print STDOUT "\n";
  #print STDOUT "\nexit=>$message";
  exit;
}

sub execute_hgt{
    my ($cmd) = @_;
    my $retour = 0;
    system($cmd); #print STDOUT system($cmd);
}

sub print_result{
    my $nbHGT2=0;
    my $newGroup=0;
    my $cpt=1;
    my @tmp_tab = split(",",$hgt_tab[0]);
    
	print OUT	"=================================================================================\n";
	print OUT	"| Program : HGT Detection 3.2 - November, 2009                                  |\n";
    print OUT   "| Authors   : Alix Boc and Vladimir Makarenkov (Universite du Quebec a Montreal)|\n";
	print OUT	"| This program computes a unique scenario of horizontal gene transfers (HGT) for|\n"; 
    print OUT   "| the given pair of species and gene phylogenetic trees.                        |\n";
	print OUT	"=================================================================================\n";
	
    print OUT "\nSpecies tree :\n". $trees_tab[0] . "\nGene Tree :\n" . $trees_tab[1];
                   
    print OUT "\n\n=============================================";
	  print OUT "\n= Criteria values before the computation ";
	  print OUT "\n=============================================";	
	if($bootstrap eq "yes"){
	  printf (OUT "\nRobinson and Foulds distance (RF) = %d",$tmp_tab_init[0]);
	  printf (OUT "\nLeast-squares coefficient(LS)     = %1.3lf",$tmp_tab_init[1]);
	  printf (OUT "\nBipartition dissimilarity         = %1.1lf\n",$tmp_tab_init[2]);
	}
	else{
	  printf (OUT "\nRobinson and Foulds distance (RF) = %d",$tmp_tab[0]);
	  printf (OUT "\nLeast-squares coefficient(LS)     = %1.3lf",$tmp_tab[1]);
	  printf (OUT "\nBipartition dissimilarity         = %1.1lf\n",$tmp_tab[2]);
	}
	
	printf(OUT "\n\nBootstrap values were computed with %d gene trees",$nbTrees) if($bootstrap eq "yes");
 
    print OUT "\n\n";
    foreach my $elt( @hgt_pos){
        if(($newGroup == 0 ) && ($mode eq 'mode=multicheck')){
            print OUT "\n================================================================"; 
            if($hgt_nbHGT_tab{"$elt"} == 1){
                print OUT "\n| Iteration #$cpt : ". $hgt_nbHGT_tab{"$elt"} ." HGT was found";
            }
            else{
              print OUT "\n| Iteration #$cpt : ". $hgt_nbHGT_tab{"$elt"} ." HGTs were found";
            }
            
            print OUT "\n================================================================";
            print OUT "\n|";
            $newGroup = 1;
            $cpt++; 
        }
        else{
            if($mode eq 'mode=monocheck'){  
                print OUT "\n================================================================";         
            }
        }
        print OUT "\n| "  . $hgt_number_tab{"$elt"};

		printf(OUT "(bootstrap value = %3.1lf%%) ",$hgt_compteur_tab{$elt}*100/$nbTrees,$hgt_compteur_tab{$elt}, $nbTrees) if(($bootstrap eq "yes")&&($hgt_number_tab{"$elt"} !~ "Trivial"));

		print OUT "\n| "  . $hgt_description_tab{"$elt"};
        print OUT "\n| "  . $hgt_criterion_tab{"$elt"};
        if($mode eq 'mode=monocheck'){
            print OUT "\n================================================================\n"; 
        }
        else{
            print OUT "\n| "; 
        }
        my $tmp = "HGT " . $hgt_nbHGT_tab{"$elt"} . " / " . $hgt_nbHGT_tab{"$elt"} . " ";
        my $tmp2 = $tmp . " Trivial";
        
        if(($mode eq 'mode=multicheck') && (( $tmp =~ $hgt_number_tab{"$elt"}) ||($tmp2 =~ $hgt_number_tab{"$elt"}))){
            print OUT "\n================================================================";
            print OUT "\n| After this iteration the criteria values are as follows :";
            print OUT "\n| " . $hgt_pos2[$nbHGT2++] ;
            print OUT "\n================================================================\n";
            $newGroup=0; 
        }
    } 
    
    print OUT "\nTotal number of HGTs : $total_hgt ";
    print OUT "(". ($total_hgt-$total_trivial) ." regular + " . $total_trivial . " trivial HGTs)" if( $total_trivial > 0);
    
    $val_retour = $total_hgt;
	
	open(OUTWEB,">>$outputWeb");
	if($bootstrap eq "yes"){
		print OUTWEB "\nbootHGT=";
		my $first=0;
		foreach my $elt( @hgt_pos){
			
			if(($bootstrap eq "yes")&&($hgt_number_tab{"$elt"} !~ "Trivial")){
				if($first==0){
					printf(OUTWEB "%3.0lf",$hgt_compteur_tab{$elt}*100/$nbTrees);
				}
				else{
					printf(OUTWEB ",%3.0lf",$hgt_compteur_tab{$elt}*100/$nbTrees);
				}
				$first=1;
			}
		}
	}
	close OUTWEB;
}


sub print_title{
	print STDOUT "============================================================================\n";
	print STDOUT "| HGT-DETECTION V.3.2 (November, 2009) by Alix Boc and Vladimir Makarenkov |\n"; 
	print STDOUT "============================================================================\n";
}

sub print_minidoc{
	print STDOUT "\nCheck the file $log_file for the computation details";
	print STDOUT "\nCheck the file $outputfile for the program output\n";
}

sub print_description{
	print STDOUT	"=================================================================================\n";
	print STDOUT	"| Program : HGT Detection 3.2 - November, 2009                                  |\n";
    print STDOUT    "| Authors   : Alix Boc and Vladimir Makarenkov (Universite du Quebec a Montreal)|\n";
	print STDOUT	"| This program computes a unique scenario of horizontal gene transfers (HGT) for|\n"; 
    print STDOUT    "| the given pair of species and gene phylogenetic trees.                        |\n";
	print STDOUT	"=================================================================================\n";
}

sub print_help{
	print STDOUT "\nUsage :\nperl run_hgt.pl -inputfile=[inputfilename] -outputfile=[outputfilename] -criterion=[rf|ls|bd]";
	print STDOUT "-speciesroot=[midpoint|file] -generoot=[midpoint|file|bestbipartition]";
	print STDOUT "-scenario=[unique|multiple] -nbhgt=[maxhgt] -path=[path] -bootstrap=[no|yes]";
	print STDOUT "\n\nsee README.txt file for more detail.";

}
