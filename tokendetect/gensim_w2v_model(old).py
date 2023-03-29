import os
from gensim.models import Word2Vec
from util import replace_code

Vecsize = 5


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
	print(model.get_latest_training_loss())
	if os.path.exists(outpath):
		os.remove(outpath)
	model.save(outpath)


if __name__ == '__main__':
	cwe = 'CWE23'
	path0 = r'D:\Desktop\hybrid-SVD\datasrc\{}\{}_bad\dsm_extract\\'.format(cwe, cwe)
	path1 = r'D:\Desktop\hybrid-SVD\datasrc\{}\{}_good\dsm_extract\\'.format(cwe, cwe)
	path_out = r'w2vmodel\{}'.format(cwe)
	Corpus = file2corpus(path0)
	Corpus += file2corpus(path1)
	word2vec_model(Corpus, Vecsize, path_out)
