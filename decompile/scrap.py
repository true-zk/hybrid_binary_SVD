import os

path_base = r'D:\retdec\CWE23\bad_res'
os.chdir(path_base)

for file in os.listdir(path_base):
    if os.path.isfile(file):
        os.remove(file)

