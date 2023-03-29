# train a token.txt 2 w2v model
# input file_token_name
# input model_name
import os
from gensim.models import word2vec


def train(file_token_name, model_name):
    path_token = r'D:\Desktop\hybrid-SVD\w2v_cfg\token_out' + '\\' + file_token_name
    path_out = r'D:\Desktop\hybrid-SVD\w2v_cfg\model_out' + '\\' + model_name
    if not os.path.exists(path_token):
        print("token.txt is not exist! error. plz generate a token.txt first")
        return None

    print(f"tokens from {path_token}\n")
    tokens = word2vec.Text8Corpus(path_token)
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
                              epochs=64)
    print(f"finish. all_loss is {model.get_latest_training_loss()}")
    model.save(path_out)


# if __name__ == '__main__':
#     train()
    # model = word2vec.Word2Vec.load(path_out + '\\w2v256.model')
    # print(model.wv['{'])
    # print(len(model.wv['{']))
    # print(model.wv.most_similar('{', topn=10))
