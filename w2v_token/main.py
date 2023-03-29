# from dsm files 2 w2v which will be used by instruction2vec
# 1 preextract the .dsm files to get the main func
# 2 gensim_w2v_model to generate corpus and train a w2v model
# e.g. w2v_CWE23.model or w2v_multi.model
from preextract import preextract
from gensim_w2v_model import train


if __name__ == '__main__':
	CWE_list = [23, 126, 127, 190, 401]
	print("===preextract CWEs", CWE_list)
	# flag=0 如果已存在提取好的dsm则跳过
	# flag=1 无论是否存在已提取好的dsm都重新提取！
	preextract(CWE_list, flag=1)
	print("===train w2v CWEs", CWE_list)
	train(CWE_list)
	for CWE in CWE_list:
		train([CWE])
