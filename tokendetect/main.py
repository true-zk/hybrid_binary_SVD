from instruction2vec import instruction2vec_
import gensim
import os

if __name__ == '__main__':
	cwe = 'CWE23'
	path0 = r'D:\Desktop\hybrid-SVD\datasrc\{}\{}_bad\dsm_extract\\'.format(cwe, cwe)
	path1 = r'D:\Desktop\hybrid-SVD\datasrc\{}\{}_good\dsm_extract\\'.format(cwe, cwe)
	path_model = r'w2vmodel\{}'.format(cwe)
	Vecsize = 5
	Model = gensim.models.Word2Vec.load(path_model)

