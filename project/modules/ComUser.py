from GeneFasta import GeneFasta
from arrays import DynamicArray
import msvcrt


class ComUser:
    """The class communicate with the user and controls the whole work"""
    def __init__(self):
        """Initialises the attributes and call starting functions"""
        self.db_lst = DynamicArray()
        self.get_db_lst()
        self.start()
        while True:
            ch = msvcrt.getch()
            if ch == b'\r':
                break

    @staticmethod
    def start():
        """Prints the starting text"""
        file = open("../text/StartText.txt")
        lines = file.readlines()
        for i in lines:
            print(i, end="")
        print("\n")

    def get_gene_name(self, n=""):
        """Asks user the name of gene he/she wants to analyse.
        Returns the given name.
        Raises exception if that name is not valid."""
        if n == "":
            n = input("Please enter a gene to analyse (ex. AT1G36060): ")
        gene = GeneFasta(n)
        try:
            gene.get_gene_id()
            return gene
        except Exception:
            print("No genes found with name:\"" + gene.gene_name + "\"")
            return self.get_gene_name()

    def get_db_lst(self):
        """Makes the list of available databases"""
        file = open("../text/DataBases.txt")
        lines = file.readlines()
        for line in lines:
            tup = tuple(line.split(" | "))
            self.db_lst.append(tup)
        return self.db_lst

    def get_db_number(self, numb1=""):
        """Asks user the number of database he/she wants to analyse at.
        Returns the given number.
        If that number is not valid, asks again."""
        if numb1 == "":
            print("Please choose the database of organism you want your gene to compare with:")
            for i in range(len(self.db_lst)):
                datab = self.db_lst[i][0]
                print(str(i+1) + ") " + datab)
            numb1 = input("Enter a number of your database: ")
        if int(numb1) > len(self.db_lst):
            print("The number is not valid!")
            numb1 = self.get_db_number()
        return int(numb1)

    def get_db_str(self, number):
        """Returns the part of link to database."""
        datab = self.db_lst[number-1][1]
        return datab

#
# if __name__ == "__main__":
#     c = ComUser()
#     g = c.get_gene_name()
#
#     numb = c.get_db_number()
#     db = c.get_db_str(numb)
#     fasta_Link = g.get_fasta_link()
#     fasta_ = g.get_fasta_()
#     blast_rid = g.get_blast_rid(numb, db)
#     blast = g.get_blast_res()
#     print(blast)
#     f = open("result1.html", "w")
#     f.write(blast)
#     f.close()
