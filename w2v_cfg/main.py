import os

from dot2token import dot2token
from word2vec import train


def multi(CWE_list):
	print("===start multi dot 2 w2v for CWEs", CWE_list)
	file_token_name = 'token_multi.txt'
	for CWE in CWE_list:
		CWE = str(CWE)
		path = r'D:\Desktop\hybrid-SVD\datasrc\CWE{}'.format(CWE)
		path0 = path + r'\goodres\dot'
		path1 = path + r'\badres\dot'

		print("path:", path0, path1, "2 token.txt:", file_token_name)
		dot2token(path0, file_token_name)
		dot2token(path1, file_token_name)

	model_name = 'w2v_multi.model'
	print("train w2v model:", model_name)
	train(file_token_name, model_name)
	print("===end multi dot 2 w2v for CWEs", CWE_list)


def binary(CWE):
	CWE = str(CWE)
	print("===start binary dot 2 w2v for CWE", CWE)

	file_token_name = 'token_CWE{}.txt'.format(CWE)
	path = r'D:\Desktop\hybrid-SVD\datasrc\CWE{}'.format(CWE)
	path0 = path + r'\goodres\dot'
	path1 = path + r'\badres\dot'

	if os.path.exists(r'D:\Desktop\hybrid-SVD\w2v_cfg\token_out' + '\\' + file_token_name):
		os.remove(r'D:\Desktop\hybrid-SVD\w2v_cfg\token_out' + '\\' + file_token_name)

	print("path:", path0, path1, "2 token.txt:", file_token_name)
	dot2token(path0, file_token_name)
	dot2token(path1, file_token_name)

	model_name = 'w2v_CWE{}.model'.format(CWE)
	print("train w2v model:", model_name)
	train(file_token_name, model_name)
	print("===end binary dot 2 w2v for CWE", CWE)


if __name__ == '__main__':
	CWE_list = [23, 126, 127, 190, 401]
	multi(CWE_list)
	for CWE_ in CWE_list:
		binary(CWE_)
