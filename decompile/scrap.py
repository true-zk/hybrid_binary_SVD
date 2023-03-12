import os
import re

# 匹配good bad的dot数量
# 注意 每个不同的CWE似乎其结构都不太一样 这个不能通用 需要按照CWE的dot文件具体情况改 例如401每个都有个纯good.dot 但是23没有
CWE = 401
CWE = 'CWE' + str(CWE)
path_old = r"D:\Desktop\hybrid-SVD\datasrc" + '\\' + CWE + '\\goodres\\dot_origin'
path = r"D:\Desktop\hybrid-SVD\datasrc" + '\\' + CWE + '\\goodres\\dot'

os.rename(path, path_old)
os.mkdir(path)

k = 0
for file in os.listdir(path_old):
    if re.search(r'good\.dot\Z', file):
        new = os.path.join(path, file)
        file = os.path.join(path_old, file)
        os.system('cp ' + file + ' ' + new)
        k += 1

print(k)

