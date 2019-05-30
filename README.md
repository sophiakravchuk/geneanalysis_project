# geneanalysis_project
This project is aimed to help biology scientists to analyze genetical information and do the genetical researches. It will find the similarity between genes and databases of genomes quickly and easily for user. For more specific information see wiki.
All the scientific information will be taken from https://www.ncbi.nlm.nih.gov/, which allows to access their databases and to run BLAST on it.
User needs to provide these kind of parameters:
-name of the gene to analyse;
- the database;
After providing the right kind of information user has to wait till the results will be given. If the process is longer then 300 seconds the program raises the error with the text “Time out for blasting!”.
If some of the information was invalid, user will get a message about it and will need to enter the information again.
The result will be printed and also user can save the html-file with all the information.
Program structure:
-The main module is called geneanalysis_project_run.py
-The classes, which I am using are in modules named arrays.py, ComUser.py and GeneFasta.py. These modules are tested in test_classes.py
-All the additional functions are in module named blast_results.py

Instructions of using the program.
Step 1.
There will be text describing the program printed and user has to press Enter to start.
The text printed:
“Hello! It is the gene analytic program!
This program allows you easily receive the report of blasting the genes.
BLAST or Basic Local Alignment Search Tool finds regions of similarity between biological sequences.
The program compares nucleotide or protein	sequences to sequence databases and calculates the statistical significance.
BLAST can be used to infer functional and evolutionary relationships between sequences
as well as help identify members of gene families.
Press Enter to start!”
Step 2 
The user will has to enter the name of the gene to analyze.
Step 3 
There will be printed a list of databases of organisms. The user will has to enter the number of the database to analyse.
 Step 4 
The user has to wait. There will be printing “Blasting... Will get result in 3 seconds” each 3 seconds. If the result is not ready in 300 seconds the program raises error with the text “Time is out for blasting!”
Documentation
Documentation is located in docs folder.  

