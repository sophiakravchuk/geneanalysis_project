import os.path
import sys
from unittest import TestCase
from GeneFasta import GeneFasta
from ComUser import ComUser
from arrays import DynamicArray, Array


class TestComUser(TestCase):
    def setUp(self):
        self.c = ComUser()

    def test_get_gene_name(self):
        gene = self.c.get_gene_name("AT1G36060")
        self.assertTrue(type(gene) == GeneFasta)
        self.assertTrue(str(gene.gene_name) == 'AT1G36060')

    def test_get_db_lst(self):
        self.assertTrue(type(self.c.get_db_lst()) == DynamicArray)

    def test_get_db_number(self):
        self.assertTrue(self.c.get_db_number("1") == 1)

    def test_get_db_str(self):
        self.assertTrue(type(self.c.get_db_str(1)) == str)


class TestGeneFasta(TestCase):
    def setUp(self):
        self.g = GeneFasta("AT1G36060")
        self.rid = ""

    def test_init(self):
        self.assertEqual(self.g.gene_name, "AT1G36060")
        self.assertEqual(self.g.db, "")
        self.assertEqual(self.g.gene_id, "")
        self.assertEqual(self.g.fasta_link, "")
        self.assertEqual(self.g.fasta_, "")
        self.assertEqual(self.g.blast_rid, "")
        self.assertEqual(self.g.blast_res, "")

    def test_get_html(self):
        file_cache = "HTMLCache_" + self.g.gene_name + ".html"
        self.assertFalse(os.path.isfile("cache/" + file_cache))
        contents_f = self.g.get_html("https://www.ncbi.nlm.nih.gov/gene/?term=" + self.g.gene_name, self.g.gene_name)
        self.assertTrue(os.path.isfile("cache/" + file_cache))
        contents_f = str("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + contents_f)

        file = open("cache/" + file_cache, "rb")
        contents = file.read()
        contents = contents.decode('utf-8')
        self.assertEqual(contents_f, contents)

    def test_request_html(self):
        file_cache = "HTMLCache_" + self.g.gene_name + ".html"
        data = {'RID': "EV7PEKGY01R",
                'CMD': 'Get',
                'FORMAT_TYPE': 'Text'}
        contents_f = self.g.request_html(True, "https://blast.ncbi.nlm.nih.gov/Blast.cgi", data, self.g.gene_name)
        contents_f = str("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + contents_f)
        file = open("cache/" + file_cache, "rb")
        contents = file.read()
        contents = contents.decode('utf-8')
        self.assertEqual(contents_f, contents)

        data = {'QUERY': "AAACTGAC",
                'PROGRAM': 'blastn',
                'CMD': 'Put',
                'DATABASE': "GPIPE/9606/current/all_top_level"}
        contents = self.g.request_html(False, "https://blast.ncbi.nlm.nih.gov/Blast.cgi", data, "")
        self.assertEqual(type(contents), str)

    def test_param_value_from_link(self):
        self.assertEqual(self.g.param_value_from_link("http://asdf.com/link?param1=222&param2=111", "param1"), "222")
        self.assertEqual(self.g.param_value_from_link("http://asdf.com/link?param1=222&param2=111", "param2"), "111")

    def test_gene_name_to_id(self):
        self.assertEqual(self.g.gene_name_to_id(), "840510")
        g_temp = GeneFasta("")
        with self.assertRaises(Exception):
            g_temp.gene_name_to_id()

    def test_gene_id_to_fasta_link(self):
        with self.assertRaises(Exception):
            self.g.gene_id_to_fasta_link()
        self.g.get_gene_id()
        self.assertEqual(self.g.gene_id_to_fasta_link(), "/nuccore/NC_003070.9?report=fasta&from=13454496&to=13456336&strand=true")

    def test_gene_fasta_from_fasta_link(self):
        with self.assertRaises(Exception):
            self.g.gene_fasta_from_fasta_link()
        self.g.get_gene_id()
        self.g.get_fasta_link()
        self.assertTrue(type(self.g.gene_fasta_from_fasta_link()), str)

    def test_rid_from_fasta(self):
        self.rid = self.g.rid_from_fasta(1, "GPIPE/9606/current/all_top_level")
        self.assertEqual(type(self.rid), str)

    def test_blast_text_from_rid(self):
        self.assertEqual(type(self.g.blast_text_from_rid(self.rid, cached=False)), str)

    def test_get_gene_id(self):
        gene_id = self.g.gene_name_to_id()
        self.assertEqual(gene_id, self.g.get_gene_id())

    def test_get_fasta_link(self):
        self.g.get_gene_id()
        fasta_link = self.g.gene_id_to_fasta_link()
        self.assertEqual(fasta_link, self.g.get_fasta_link())

    def test_get_fasta_(self):
        self.g.get_gene_id()
        self.g.get_fasta_link()
        fasta_ = self.g.gene_fasta_from_fasta_link()
        self.assertEqual(fasta_, self.g.get_fasta_())

    def test_get_db(self):
        self.g.get_db("GPIPE/9606/current/all_top_level")

    def test_get_blast_rid(self):
        blast_rid = self.g.rid_from_fasta(1, "GPIPE/9606/current/all_top_level")
        self.assertEqual(blast_rid, self.g.get_blast_rid(1, "GPIPE/9606/current/all_top_level"))


class TestArray(TestCase):
    def setUp(self):
        self.arr = Array(5)

    def test_init(self):
        with self.assertRaises(ValueError):
            arr = Array(-1)
        self.assertEqual(self.arr._size, 5)
        for i in range(len(self.arr._elements)):
            self.assertTrue(self.arr._elements[i] is None)

    def test_len(self):
        self.assertEqual(self.arr._size, len(self.arr))

    def test_getitem(self):
        self.assertEqual(self.arr[0], self.arr._elements[0])
        with self.assertRaises(IndexError):
            el = self.arr[-1]

    def test_setitem(self):
        self.arr[0] = "a"
        self.assertEqual(self.arr[0], "a")
        with self.assertRaises(IndexError):
            self.arr[-1] = "a"

    def test_clear(self):
        self.arr[0] = "a"
        self.assertEqual(self.arr[0], "a")
        self.arr.clear(None)
        for i in range(len(self.arr._elements)):
            self.assertTrue(self.arr._elements[i] is None)

    def test_str(self):
        self.assertEqual(type(str(self.arr)), str)


class TestDynamicArray(TestCase):
    def setUp(self):
        self.arr = DynamicArray()
        self.arr.append("a")

    def test_init(self):
        self.assertEqual(self.arr._n, 1)

    def test_len(self):
        self.assertEqual(self.arr._n, len(self.arr))

    def test_getitem(self):
        self.assertEqual(self.arr[0], self.arr._A[0])
        with self.assertRaises(IndexError):
            el = self.arr[-1]

    def test_append(self):
        self.arr.append("b")
        self.assertEqual(self.arr[0], "a")
        self.assertEqual(self.arr[1], "b")
        self.assertEqual(len(self.arr), 2)

    def test_resize(self):
        self.arr._resize(3)
        self.assertEqual(self.arr._A._size, 3)

    def test_make_array(self):
        self.assertEqual(type(self.arr._make_array(4)), Array)

    def test_insert(self):
        self.arr._resize(1)
        self.arr.insert(0, "A")
        self.assertEqual(self.arr._A._size, 2)
        self.assertEqual(self.arr._A[0], "A")
        self.assertEqual(self.arr._n, 2)

    def test_remove(self):
        with self.assertRaises(ValueError):
            self.arr.remove("b")
        self.arr.insert(1, "A")
        self.arr.remove("a")
        self.assertEqual(self.arr._n, 1)

    def test_str(self):
        self.assertEqual(type(str(self.arr)), str)

    def test_pop(self):
        self.arr.insert(1, "A")
        last = self.arr._A[self.arr._n - 1]
        self.assertEqual(self.arr.pop(), last)
        self.assertEqual(self.arr._n, 1)

    def test_clear(self):
        self.assertEqual(self.arr[0], "a")
        self.arr.clear()
        for i in range(len(self.arr._A)):
            self.assertTrue(self.arr._A[i] is None)
        self.assertTrue(self.arr._n == 0)
