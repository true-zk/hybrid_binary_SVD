import re
import os
from gensim.models import word2vec

path_base = os.getcwd()
path_out = path_base + '\\model_out'
path_token = path_base + '\\token_out\\token.txt'

def train():
    print(f"tokens from {path_token}\n")
    tokens = word2vec.Text8Corpus(path_token)
    print(tokens)
    print('token to vec train\n')
    model = word2vec.Word2Vec(tokens, sg=0,  # CBOW
                              vector_size=256,
                              window=3,
                              min_count=3,
                              compute_loss=True,
                              negative=3,
                              sample=0.001,
                              hs=1,
                              workers=4,
                              epochs=1)
    print(f"finish. loss is {model.get_latest_training_loss()}")
    model.save(path_out + '\\w2v256.model')


if __name__ == '__main__':
    # train()
    model = word2vec.Word2Vec.load(path_out + '\\w2v256.model')
    print(model.wv['{'])
    print(len(model.wv['{']))
    print(model.wv.most_similar('{', topn=10))
