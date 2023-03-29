import re
import os


# decompile good; output in path_goodres
def decompile_good():
    path_goodres = path_cwe23 + r"\good_res"
    if os.path.exists(path_goodres):
        os.system('rm -rf ' + path_goodres)
    os.mkdir(path_goodres)
    path_good_dot = path_goodres + r'\dot'  # .dot
    os.mkdir(path_good_dot)
    path_good_dc = path_goodres + r'\dc'  # decompile c
    os.mkdir(path_good_dc)
    path_good_dsm = path_goodres + r'\dsm'  # .dsm
    os.mkdir(path_good_dsm)

    for file in good_list:
        file_path = path_good + '\\' + file
        os.system("python " + path_de + ' --backend-emit-cfg ' + file_path + ' --output ' + path_goodres + '\\' + file)

    os.chdir(path_goodres)
    for file in os.listdir(path_goodres):
        if re.search(r'good\Z', file):
            os.system('mv ' + file + ' ' + path_good_dc)
        if re.search('goodG2B', file) and re.search(r'\.dot\Z', file):
            os.system('mv ' + file + ' ' + path_good_dot)
        if re.search(r'\.dsm\Z', file):
            os.system('mv ' + file + ' ' + path_good_dsm)


# decompile bad; output in path_badres
def decompile_bad():
    path_badres = path_cwe23 + r"\bad_res"
    if os.path.exists(path_badres):
        os.system('rm -rf ' + path_badres)
    os.mkdir(path_badres)
    path_bad_dot = path_badres + r'\dot'  # .dot
    os.mkdir(path_bad_dot)
    path_bad_dc = path_badres + r'\dc'  # decompile c
    os.mkdir(path_bad_dc)
    path_bad_dsm = path_badres + r'\dsm'  # .dsm
    os.mkdir(path_bad_dsm)

    for file in bad_list:
        file_path = path_bad + '\\' + file
        os.system("python " + path_de + ' --backend-emit-cfg ' + file_path + ' --output ' + path_badres + '\\' + file)
        os.chdir(path_badres)
        for tmpfile in os.listdir(path_badres):
            if re.search(r'bad\Z', tmpfile):
                os.system('mv ' + tmpfile + ' ' + path_bad_dc)
            elif re.search('badEv', tmpfile) and re.search(r'\.dot\Z', tmpfile):
                os.system('mv ' + tmpfile + ' ' + path_bad_dot)
            elif re.search(r'\.dsm\Z', tmpfile):
                os.system('mv ' + tmpfile + ' ' + path_bad_dsm)
            elif os.path.isfile(tmpfile):
                os.system('rm ' + tmpfile)


if __name__ == '__main__':
    path_base = os.getcwd()
    path_de = path_base + r"\bin\retdec-decompiler.py"
    path_cwe23 = path_base + r"\CWE23"
    path_good = path_cwe23 + r"\good"
    path_bad = path_cwe23 + r"\bad"
    good_list = os.listdir(path_good)
    bad_list = os.listdir(path_bad)
    decompile_bad()





