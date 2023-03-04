import os
import re

# 匹配good bad的dot数量
path = r"D:\Desktop\hybrid-SVD\CWE23_good\dot_origin"
path_new = r'D:\Desktop\hybrid-SVD\CWE23_good\dot'
k = 0
os.chdir(path)
for file in os.listdir(path):
    if re.search('goodG2B1Ev', file):
        tmp = file.replace('goodG2B1Ev', 'goodG2BEv')
        new_file = path_new + '\\' + tmp
        os.system('cp ' + file + ' ' + new_file)
        k += 1
    elif re.search('goodG2BEv', file):
        new_file = path_new + '\\' + file
        os.system('cp ' + file + ' ' + new_file)
        k += 1
print(k)

