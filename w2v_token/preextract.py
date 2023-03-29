import os
import re
import shutil


def extract_one_file(path_in, path_out, pattern):
    with open(path_in, 'r') as f:
        lines = f.readlines()
        tag = None

        for line in lines:
            if re.search(r'goodB2G[1-9]+|goodB2G |goodG2B[1-9]+|goodG2B ', line) or re.search(pattern, line):
                lines = lines[lines.index(line):]
                for line0 in lines:
                    if re.search('ret', line0):
                        tag = re.search('ret', line0).start()
                        lines = lines[:lines.index(line0) + 1]
                        break
                break

        for i, line in enumerate(lines):
            lines[i] = lines[i].replace(lines[i][0: tag], '')
        lines = lines[1:]

        with open(path_out, 'w') as f0:
            f0.writelines(lines)


# flag=0 如果已存在提取好的dsm则跳过
# flag=1 无论是否存在已提取好的dsm都重新提取！
def preextract_(CWE, flag=0):
    print("---preextract CWE", CWE, "---flag=", flag)

    CWE = str(CWE)
    path0 = r'D:\Desktop\hybrid-SVD\datasrc\CWE{}\badres\dsm\\'.format(CWE)
    path_new0 = r'D:\Desktop\hybrid-SVD\datasrc\CWE{}\badres\dsm_extract\\'.format(CWE)
    path1 = r'D:\Desktop\hybrid-SVD\datasrc\CWE{}\goodres\dsm\\'.format(CWE)
    path_new1 = r'D:\Desktop\hybrid-SVD\datasrc\CWE{}\goodres\dsm_extract\\'.format(CWE)

    if flag == 1:
        if os.path.exists(path_new0):
            shutil.rmtree(path_new0)
        if os.path.exists(path_new1):
            shutil.rmtree(path_new1)

    if os.path.exists(path_new0) and os.path.exists(path_new1):
        print("already exist dsm_extract. plz check if need preextract dsm???")
        return

    os.mkdir(path_new0)
    os.mkdir(path_new1)

    cwe = 'CWE{}_'.format(CWE)
    for file in os.listdir(path0):
        Pattern = file.replace(cwe, '')
        Pattern = Pattern.split('__')[0]
        extract_one_file(path0+file, path_new0+file, Pattern)

    for file in os.listdir(path1):
        Pattern = file.replace(cwe, '')
        Pattern = Pattern.split('__')[0]
        extract_one_file(path1+file, path_new1+file, Pattern)


# flag=0 如果已存在提取好的dsm则跳过
# flag=1 无论是否存在已提取好的dsm都重新提取！
def preextract(CWE_list, flag=0):
    for CWE in CWE_list:
        preextract_(CWE, flag)

