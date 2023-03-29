import os
import shutil


def recover(path):
	path_dot = path + '\\' + 'dot_old'
	path_dsm = path + '\\' + 'dsm_old'
	if os.path.exists(path_dsm) and os.path.exists(path_dot):
		shutil.rmtree(path + r'\dot')
		shutil.rmtree(path + r'\dsm')
		os.rename(path_dot, path + r'\dot')
		os.rename(path_dsm, path + r'\dsm')


# input the CWE num in the list
if __name__ == '__main__':
	CWE_list = [23, 126, 127, 190, 401]
	for CWE in CWE_list:
		CWE = 'CWE' + str(CWE)
		Path = r"D:\Desktop\hybrid-SVD\datasrc" + '\\' + CWE
		path_good = Path + '\\' + 'goodres'
		path_bad = Path + '\\' + 'badres'
		recover(path_bad)
		recover(path_good)