import time
import urllib.request
import lxml.html as html
import os.path
import hashlib
import requests


class GeneFasta:
    """The class that does all the work"""
    def __init__(self, gene_name):
        """Initialises the attributes
        :param gene_name: the name of gene user wants to analyse
        """
        self.gene_name = gene_name
        self.db = ""
        self.gene_id = ""
        self.fasta_link = ""
        self.fasta_ = ""
        self.blast_rid = ""
        self.blast_res = ""

    @staticmethod
    def get_html(link, link_id):
        """
        Gets the information by the link.
        Checks whether that file is already in cache and
        if it is gets information from it,
        if it is not gets the information by the link.
        :param link: the link to the information
        (link to the gene, link to the database, link to the fasta etc.)
        :param link_id: the id for link (for the cachefile name)
        (name of the gene, code of database, id of fasta etc.)
        """
        file_cache = "HTMLCache_" + link_id + ".html"
        if os.path.isfile("../cache/" + file_cache):
            file = open("../cache/" + file_cache, "rb")
            contents = file.read()
            file.close()
        else:
            response = urllib.request.urlopen(link)
            if response is None:
                raise Exception("No internet connection")
            contents = response.read()
            file = open("../cache/" + file_cache, "wb")
            file.write(contents)
            file.close()
        contents = contents.decode('utf-8')
        header = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
        headerpos = contents.find(header)
        if headerpos >= 0:
            contents = contents[len(header):]
        return contents

    @staticmethod
    def request_html(is_get, link, params, cache_id):
        """
        Gets the information by the link with the method get or put.
        Checks whether that file is already in cache and
        if it is gets information from it,
        if it is not gets the information by the link.
        :param is_get: True if the method to use is get and False if the method is put
        :param link: link to the NCBI Blast
        :param params: a dictionary of parameters for link (QUERY, PROGRAM, CMD, DATABASE)
        :param cache_id: id for cachefile
        :return: information
        """

        use_cache = cache_id != ""

        file_cache = "HTMLCache_" + cache_id + ".html"
        if use_cache and os.path.isfile("../cache/" + file_cache):
            file = open("../cache/" + file_cache, "rb")
            contents = file.read()
            file.close()
        else:
            if is_get:
                response = requests.get(link, params)
            else:
                response = requests.put(link, params)

            if response is None:
                raise Exception("No internet connection")
            contents = response.content
            if use_cache and len(contents) > 10:
                file = open("../cache/" + file_cache, "wb")
                file.write(contents)
                file.close()
        contents = contents.decode('utf-8')
        header = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
        headerpos = contents.find(header)
        if headerpos >= 0:
            contents = contents[len(header):]
        return contents

    @staticmethod
    def param_value_from_link(link, param_name):
        """
        Gets the value of parameter from the link.
        example: return 222 by call("http://asdf.asdf.com/link?param1=222&param2=111", "param1")
        :param link: the link to work with
        :param param_name: the name of parameter
        :return: parameter value
        """
        param_pos = link.find(param_name)
        if param_pos < 0:
            raise Exception("Invalid param")
        sub_link = link[param_pos + len(param_name) + 1:]
        param_pos = sub_link.find("&")
        if param_pos >= 0:
            sub_link = sub_link[:param_pos]
        return sub_link

    def gene_name_to_id(self):
        """
        Gets the link to the gene by its name.
        Raises the exception if there is no gene with such a name.
        Raises the exception if there is no link for this gene name.
        :return: link to the gene
        """
        contents = self.get_html("https://www.ncbi.nlm.nih.gov/gene/?term=" + self.gene_name, self.gene_name)
        search_page = html.document_fromstring(contents)
        genes_list = search_page.find_class("gene-name-id")
        if len(genes_list) == 0:
            raise Exception("No genes found with name:\"" + self.gene_name + "\"")
        for gene in genes_list:
            gene_html = gene.text_content()
            if gene_html.find(self.gene_name) >= 0:
                for link in gene.iterlinks():
                    link_href = link[2]
                    if link_href.find("/gene/") >= 0:
                        link_href = link_href[link_href.find("/gene/") + len("/gene/"):]
                        return link_href
        raise Exception("Internal error, can not found gene link:\"" + self.gene_name + "\"")

    def gene_id_to_fasta_link(self):
        """
        Gets the fasta link from gene id
        Raises exception if the fasta is not such gene link.
        Raises exception if the fasta is not found for the gene id.
        :return: the fasta link
        """
        contents = self.get_html("https://www.ncbi.nlm.nih.gov/gene/" + self.gene_id, self.gene_id)
        page = html.document_fromstring(contents)
        genes_links = page.find_class("note-link")
        if len(genes_links) == 0:
            raise Exception("No fasta link found for gene Id:\"" + self.gene_id + "\"")
        for gene in genes_links:
            for link in gene.iterlinks():
                link_href = link[2]
                if link_href.find("fasta") >= 0:
                    return link_href
        raise Exception("Internal error, can not find gene fasta link:\"" + self.gene_name + "\"")

    def gene_fasta_from_fasta_link(self):
        """
        Gets the fasta from fasta link.
        Raises the exception if no fasta link found for gene Id
        :return: gene fasta
        """
        contents = self.get_html("https://www.ncbi.nlm.nih.gov" + self.fasta_link, "fasta_" + self.gene_id)
        page = html.document_fromstring(contents)
        genes_links = page.find_class("seq gbff")
        if len(genes_links) != 1:
            raise Exception("No fasta link found for gene Id:\"" + self.gene_id + "\"")
        attrs = genes_links[0].attrib
        chr_id = attrs['val']

        nuc_from = self.param_value_from_link(self.fasta_link, "from")
        nuc_to = self.param_value_from_link(self.fasta_link, "to")
        fasta_link_direct = "id={0}&db=nuccore&report=fasta&from={1}&to={2}&strand=on&retmode=txt"\
            .format(chr_id, nuc_from, nuc_to)
        fasta_link_direct = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?" + fasta_link_direct

        contents = self.get_html(fasta_link_direct, "fasta_" + chr_id + "_from_" + nuc_from + "_to_" + nuc_to)
        return contents

    def rid_from_fasta(self, organism, db):
        """
        Gets the RID from fasta
        :param organism: number of database
        :param db: link to databases
        :return: RID
        """
        m = hashlib.md5()
        m.update((self.fasta_ + str(organism)).encode('utf-8'))
        file_key = m.hexdigest()

        data = {'QUERY': self.fasta_,
                'PROGRAM': 'blastn',
                'CMD': 'Put',
                'DATABASE': db}
        contents = self.request_html(False, "https://blast.ncbi.nlm.nih.gov/Blast.cgi", data, "rid_" + file_key)

        page = html.document_fromstring(contents)
        rid_input = page.xpath('//input[@name="RID"]')
        if len(rid_input) == 0:
            raise Exception("No RID found")
        return rid_input[0].value

    def blast_text_from_rid(self, rid, cached=False):
        """
        Gets the blast text from rid
        :param rid: RID
        :param cached: True if the inf was cached or False if it was not
        :return: the blast text
        """
        data = {'RID': rid,
                'CMD': 'Get',
                'FORMAT_TYPE': 'Text'}
        if cached:
            cache_id = "blast_" + rid
        else:
            cache_id = ""
        contents = self.request_html(True, "https://blast.ncbi.nlm.nih.gov/Blast.cgi", data, cache_id)
        return contents

    def get_gene_id(self):
        """Gets the gene ID"""
        self.gene_id = self.gene_name_to_id()
        return self.gene_id

    def get_fasta_link(self):
        """Gets the fasta link"""
        self.fasta_link = self.gene_id_to_fasta_link()
        return self.fasta_link

    def get_fasta_(self):
        """Gets the fasta"""
        self.fasta_ = self.gene_fasta_from_fasta_link()
        return self.fasta_

    def get_db(self, db_str):
        """Gets the database"""
        self.db = db_str
        return self.db

    def get_blast_rid(self, organism, db):
        """Gets the blast RID"""
        self.blast_rid = self.rid_from_fasta(organism, db)
        return self.blast_rid

    def get_blast_res(self):
        """Gets the results of blast.
        Raises exception if the time of waiting is bigger then 300 seconds"""
        count = 100
        while count > 0:
            self.blast_res = self.blast_text_from_rid(self.blast_rid, False)
            count -= 1
            if self.blast_res.find("This page will be automatically updated") > 0:
                print("Blasting... Will get result in 3 seconds")
                time.sleep(3)
            else:
                break
        if self.blast_res.find("This page will be automatically updated") > 0:
            raise Exception("Time is out for blasting!")
        filename = "../cache/" + "blast_res_"+self.blast_rid+".html"
        file = open(filename, "wb")
        file.write(self.blast_res.encode("utf-8"))
        file.close()
        return filename
