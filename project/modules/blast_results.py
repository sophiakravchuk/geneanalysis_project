def table_dct(filename, from_line="", end_line=""):
    """
    (str, str, str) -> lst

    Reads the file (filename).
    Returns a dictionary of matches and their scores EValues and max idents
    and a list of lines with table.

    e.g.
    {'NC_000007.14': (' Homo sapiens chromosome 7, GRCh38.p12 Primary Ass...',
    {'Score': '43.7', 'EValue': '0.83', 'MaxIdent': '86%'})}
    """
    lst_table = []
    dct_table = {}
    dct_one_match = {}
    with open(filename, encoding='utf-8', errors='ignore') as f:
        for line in f:
            if from_line != "":
                if line.startswith(from_line):
                    lst_table.append(from_line)
                    from_line = ""
                    continue
            if line.startswith(end_line):
                break
            if lst_table != [] and line != "\n":
                lst_table.append(line[:-2])
                name = line[:line.find(" ")]
                long_name = line[line.find(" "):line.find("...") + 3]
                line = line[line.find("...") + 3:]
                line = line.strip().split()
                dct_one_match["Score"] = line[0]
                dct_one_match["EValue"] = line[1]
                dct_one_match["MaxIdent"] = line[2]
                dct_table[name] = long_name, dct_one_match
    return dct_table, lst_table


def best_score_alignment(filename, from_line="", end_line=""):
    """
    (str, str, str) -> lst

    Reads the file (filename).
    Returns a list of lines with the alignment.
    """
    lst_alignment = []
    with open(filename, encoding='utf-8', errors='ignore') as f:
        for line in f:
            if from_line != "":
                if line.startswith(from_line):
                    from_line = ""
                    lst_alignment.append(line[:-2])
                    continue
            if line.startswith(end_line):
                break
            if lst_alignment != [] and line != "\n":
                lst_alignment.append(line[:-1])
    return lst_alignment


if __name__ == "__main__":
    dct, lst = table_dct("result1.html", "Sequences producing significant alignments:", "ALIGNMENTS")
    print(dct)
    for i in lst:
        print(i)
    lst1 = best_score_alignment("result1.html", "ALIGNMENTS\n", " Features flanking this part of subject sequence:")
    for i in lst1:
        print(i)
