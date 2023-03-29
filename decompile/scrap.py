# 匹配dot dsm数量

import os
import re
import shutil


def match_dsm_dot(path_res):
    path_dot = path_res + r'\dot'
    path_dsm = path_res + r'\dsm'

    path_dot_new = path_res + r'\dot_tmp'
    path_dsm_new = path_res + r'\dsm_tmp'
    os.mkdir(path_dsm_new)
    os.mkdir(path_dot_new)
    no_match = len(os.listdir(path_dsm))  # 没匹配的个数
    for file_dsm in os.listdir(path_dsm):
        name_pattern = file_dsm.split('.')[0]
        multi_flag = 0
        tmp = ''
        for file_dot in os.listdir(path_dot):
            if re.match(name_pattern, file_dot) and multi_flag == 1 and re.search('goodB2G|goodG2B', file_dot):
                tmp = file_dot
                break
            if re.match(name_pattern, file_dot) and multi_flag == 0:
                no_match -= 1
                tmp = file_dot
                multi_flag = 1
        if tmp != '':
            file_dot_old = os.path.join(path_dot, tmp)
            shutil.copy(file_dot_old, path_dot_new)

    if no_match == 0:
        os.rename(path_dot, path_res + r'\dot_old')
        os.rename(path_dot_new, path_dot)
        shutil.rmtree(path_dsm_new)
        return 0

    no_match = len(os.listdir(path_dot_new))

    for file_dot in os.listdir(path_dot_new):
        name_pattern = file_dot.split('.')[0]
        for file_dsm in os.listdir(path_dsm):
            if re.match(name_pattern, file_dsm):
                file_dsm_old = os.path.join(path_dsm, file_dsm)
                shutil.copy(file_dsm_old, path_dsm_new)
                no_match -= 1
                break

    if no_match == 0:
        os.rename(path_dot, path_res + r'\dot_old')
        os.rename(path_dot_new, path_dot)
        os.rename(path_dsm, path_res + r'\dsm_old')
        os.rename(path_dsm_new, path_dsm)
        return 0

    return no_match


# input the CWE num in the list
if __name__ == '__main__':
    CWE_list = [23, 126, 127, 190, 401]
    for CWE in CWE_list:
        CWE = 'CWE' + str(CWE)
        Path = r"D:\Desktop\hybrid-SVD\datasrc" + '\\' + CWE
        path_good = Path + '\\' + 'goodres'
        path_bad = Path + '\\' + 'badres'
        No_match0 = match_dsm_dot(path_good)
        No_match1 = match_dsm_dot(path_bad)
        print("no match num for CWE", CWE, " is: ", No_match1, No_match0)

# check num
# if __name__ == '__main__':
#     CWE_list = [23, 126, 127, 190, 401]
#     for CWE in CWE_list:
#         CWE = 'CWE' + str(CWE)
#         Path = r"D:\Desktop\hybrid-SVD\datasrc" + '\\' + CWE
#         path_good = Path + '\\' + 'goodres'
#         path_bad = Path + '\\' + 'badres'
#         print(len(os.listdir(path_good + '\\' + 'dot')), len(os.listdir(path_good + '\\' + 'dsm')))
#         print(len(os.listdir(path_bad + '\\' + 'dot')), len(os.listdir(path_bad + '\\' + 'dsm')))
