import os
import re


def extract_(path_in, path_out, pattern):
    with open(path_in, 'r') as f:
        lines = f.readlines()
        tag = None

        for line in lines:
            if re.search(pattern, line):
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


if __name__ == '__main__':
    path0 = r'D:\Desktop\hybrid-SVD\datasrc\CWE23\CWE23_bad\dsm\\'
    path_new0 = r'D:\Desktop\hybrid-SVD\datasrc\CWE23\CWE23_bad\dsm_extract\\'
    path1 = r'D:\Desktop\hybrid-SVD\datasrc\CWE23\CWE23_good\dsm\\'
    path_new1 = r'D:\Desktop\hybrid-SVD\datasrc\CWE23\CWE23_good\dsm_extract\\'
    for file in os.listdir(path0):
        cwe = 'CWE23_'
        Pattern = file.replace(cwe, '')
        Pattern = Pattern.split('__')[0]
        extract_(path0+file, path_new0+file, Pattern)
    for file in os.listdir(path1):
        cwe = 'CWE23_'
        Pattern = file.replace(cwe, '')
        Pattern = Pattern.split('__')[0]
        extract_(path1+file, path_new1+file, Pattern)



