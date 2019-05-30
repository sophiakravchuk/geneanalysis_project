from ComUser import ComUser
from blast_results import table_dct, best_score_alignment
import os
from shutil import copy2


c = ComUser()

g = c.get_gene_name()
numb = c.get_db_number()
db = c.get_db_str(numb)
fasta_Link = g.get_fasta_link()
fasta_ = g.get_fasta_()
blast_rid = g.get_blast_rid(numb, db)
blast = g.get_blast_res()

dct, lst = table_dct(blast, "Sequences producing significant alignments:", "ALIGNMENTS")

for i in lst:
    print(i)
print("The alignment of the best score match is:")
lst1 = best_score_alignment(blast, "ALIGNMENTS\n", " Features flanking this part of subject sequence:")

for i in lst1:
    print(i)
n = input("Do you want to save a file with full results? [y/n]")

if n == "y":
    this_path = os.getcwd()
    print("Now you are here: ", this_path)
    path = input("Enter a path (ex. ../../folder/filename) It would be better to enter .html extension:")
    copy2(blast, path)
    print("The file was successfully saved.")

print("Greate job! I am happy to help you) ")
