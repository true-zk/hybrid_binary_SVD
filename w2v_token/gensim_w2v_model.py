import os
from gensim.models import Word2Vec
from util import replace_code


def file2corpus(path):
	word_list = []
	for file in os.listdir(path):
		file = os.path.join(path, file)
		with open(file, 'r') as f:
			lines = f.readlines()
			for line in lines:
				line = replace_code(line)
				line = line.replace(',', ' ')
				line = line.split()
				word_list.append(line)
	return word_list


def word2vec_model(corpus, vecsize, outpath):
	model = Word2Vec(corpus, vector_size=vecsize, window=128, min_count=1, workers=4, epochs=10, compute_loss=True)
	print("all_loss:", model.get_latest_training_loss())
	if os.path.exists(outpath):
		os.remove(outpath)
	model.save(outpath)


def train(CWE_list):
	Corpus = []
	Vecsize = 5
	path_out = r'D:\Desktop\hybrid-SVD\w2v_token\model_out'
	if len(CWE_list) > 1:
		path_out += r'\w2v_multi.model'
	else:
		path_out += r'\w2v_CWE{}.model'.format(CWE_list[0])

	for CWE in CWE_list:
		print("---add CWE", CWE, " to Corpus")
		CWE = str(CWE)
		cwe = 'CWE{}'.format(CWE)
		path0 = r'D:\Desktop\hybrid-SVD\datasrc\{}\badres\dsm_extract\\'.format(cwe, cwe)
		path1 = r'D:\Desktop\hybrid-SVD\datasrc\{}\goodres\dsm_extract\\'.format(cwe, cwe)

		Corpus += file2corpus(path0)
		Corpus += file2corpus(path1)

	print(f"---train model. size:{Vecsize}, out_path:{path_out}")
	word2vec_model(Corpus, Vecsize, path_out)
