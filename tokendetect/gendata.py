import os
import gensim
import torch
import numpy as np
from instruction2vec import instruction2vec_


def dsm2data(dsm, label, cwe):
	data = {}
	path_model = r'D:\Desktop\hybrid-SVD\w2v_token\model_out\w2v_{}.model'.format(cwe)
	model = gensim.models.Word2Vec.load(path_model)
	for i, line in enumerate(dsm):
		vec = instruction2vec_(line, model)
		data['x'] = [vec] if 'x' not in data else data['x'] + [vec]

	for key, item in data.items():
		try:
			data[key] = torch.tensor(np.array(item), dtype=torch.float)
		except ValueError:
			print(ValueError, data)
	# data['x'] = torch.tensor(data['x'], dtype=torch.float)
	data['y'] = torch.tensor([label], dtype=torch.long)
	return data


def load_extract_dsm(path):
	for file in os.listdir(path):
		file = os.path.join(path, file)
		try:
			if os.path.basename(file).find('good') != -1:
				label = 1
				yield file, label
			elif os.path.basename(file).find('bad') != -1:
				label = 0
				yield file, label
		except FileExistsError:
			print("error", file)
			continue


def gendata(path, cwe):
	dataset = []
	for file, label in load_extract_dsm(path):
		with open(file, 'r') as f:
			data = dsm2data(f.readlines(), label, cwe)
			if data != -1:
				dataset.append(data)
	return dataset


# if __name__ == "__main__":
# 	CWE = 'CWE401'
# 	path0 = r'D:\Desktop\hybrid-SVD\datasrc\{}\badres\dsm_extract\\'.format(CWE)
# 	Dataset = gendata(path0, CWE)
# 	print(Dataset)
