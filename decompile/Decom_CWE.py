import re
import os
import shutil


def decompile_(decompiler, path_in, path_out, flag: str, cwe: str):
    path_in_ = path_in + '\\' + flag
    path_out_ = path_out + '\\' + flag + 'res'
    path_out_dot = path_out_ + '\\dot'
    path_out_dc = path_out_ + '\\dc'
    path_out_dsm = path_out_ + '\\dsm'
    if os.path.exists(path_out_):
        shutil.rmtree(path_out_)
    os.mkdir(path_out_)  # 创建输出文件夹
    os.mkdir(path_out_dot)
    os.mkdir(path_out_dsm)
    os.mkdir(path_out_dc)

    for file in os.listdir(path_in_):
        filepath = os.path.join(path_in_, file)
        os.system('python ' + decompiler + ' --backend-emit-cfg ' +
                  filepath + ' --output ' + path_out_ + '\\' + file)
        for tmpfile in os.listdir(path_out_):
            tmpfilepath = os.path.join(path_out_, tmpfile)
            if re.search(flag + r'\Z', tmpfile):
                shutil.move(tmpfilepath, path_out_dc)
            elif re.search(r'\.' + cwe, tmpfile) and re.search(r'\.dot\Z', tmpfile):
                shutil.move(tmpfilepath, path_out_dot)
            elif re.search(r'\.dsm\Z', tmpfile):
                shutil.move(tmpfilepath, path_out_dsm)
            elif os.path.isfile(tmpfilepath):
                os.remove(tmpfilepath)


def decompile(decompiler, path_in, path_out, cwe):
    decompile_(decompiler, path_in, path_out, 'good', cwe)
    decompile_(decompiler, path_in, path_out, 'bad', cwe)


if __name__ == '__main__':
    CWE = 401
    CWE = 'CWE' + str(CWE)
    path_retdec = r"D:\Develop\retdec\bin\retdec-decompiler.py"
    path_CWE_xxx = r"D:\Desktop\hybrid-SVD\datasrc" + '\\' + CWE
    decompile(path_retdec, path_CWE_xxx, path_CWE_xxx, CWE)
