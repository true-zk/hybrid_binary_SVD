# input: num of the CWExx
# data: [data_dot, data_dsm]
# data_dot=Data(x=[22, 256], edge_index=[2, 28], num_nodes=22, y=[1], cwe='CWE23')
# data_dsm=[[tensor(45)],[tensor(45)]...]
import os
import random
import re
import sys
import gensim
import pydot
import torch
import numpy as np
from torch_geometric.data import Data
from torch.utils.data import Dataset
from instruction2vec import instruction2vec_
import pickle
import matplotlib.pyplot as plt


# cwe_dic = {'1': [0, 0, 0, 0, 0, 0],
#            'CWE23': [0, 1, 0, 0, 0, 0],
#            'CWE126': [0, 0, 1, 0, 0, 0],
#            'CWE127': [0, 0, 0, 1, 0, 0],
#            'CWE190': [0, 0, 0, 0, 1, 0],
#            'CWE401': [0, 0, 0, 0, 0, 1]}
cwe_dic = {'1': 0,
           'CWE23': 1,
           'CWE126': 2,
           'CWE127': 3,
           'CWE190': 4,
           'CWE401': 5}


def gen_token(string: str):
    replace_dict = {r"\l": " ",
                    "(": " ( ",
                    ")": " ) ",
                    "[": " [ ",
                    "]": " ] ",
                    "{": " { ",
                    "}": " } ",
                    "\"": " ",
                    ",": " , ",
                    ":": " "
                    }
    for key in replace_dict:
        string = string.replace(key, replace_dict[key])
    after_replace = string.lower()
    tokens = []
    for word in after_replace.split():
        if re.match("^@.*(good|bad)", word):
            tokens.append("@func")
        else:
            tokens.append(word)
    return tokens


def dot2data(dot, cwe, label):
    model_path = r'D:\Desktop\hybrid-SVD\w2v_cfg\model_out\w2v_multi.model'
    w2vmodel = gensim.models.Word2Vec.load(model_path)

    nodes = dot[0].get_nodes()
    edges = dot[0].get_edges()
    edge_list = []

    for node in nodes:
        if "label" not in node.obj_dict["attributes"]:
            index = nodes.index(node)
            for edge in edges:
                src = edge.get_source().split(":")[0]
                dst = edge.get_destination()
                if node.get_name() == src or node.get_name() == dst:
                    del edges[edges.index(edge)]
            del nodes[index]

    for edge in edges:
        src = edge.get_source().split(":")[0]
        dst = edge.get_destination()
        src_id = None
        dst_id = None
        for node in nodes:
            # if "label" not in node.obj_dict["attributes"]:
            #     del nodes[nodes.index(node)]
            if node.get_name() == src:
                src_id = nodes.index(node)
            if node.get_name() == dst:
                dst_id = nodes.index(node)
        if src_id is not None and dst_id is not None:
            edge_list.append([src_id, dst_id])
    edge_index = torch.tensor(edge_list).t().contiguous()

    data = {}

    for i, node in enumerate(nodes):
        value = node.obj_dict["attributes"]
        if "label" in value:
            value = value["label"]
            tokens = gen_token(value)
            token_vec = np.zeros((256,), dtype=float)
            token_num = len(tokens)
            for token in tokens:
                if token in w2vmodel.wv:
                    token_vec += (w2vmodel.wv[token])
                else:
                    pass
            token_vec = token_vec / token_num
            data['x'] = [token_vec] if 'x' not in data else data['x'] + [token_vec]
        else:
            del nodes[i]

    for key, item in data.items():
        try:
            data[key] = torch.tensor(np.array(item))
        except ValueError:
            print(ValueError, data)

    data['edge_index'] = edge_index.view(2, -1).long()
    data = Data.from_dict(data)
    data.num_nodes = len(nodes)
    data.x = data.x.float()
    if label == 1:
        data.y = torch.tensor(cwe_dic['1'])
    elif label == 0 and cwe == 'CWE23':
        data.y = torch.tensor(cwe_dic['CWE23'])
    elif label == 0 and cwe == 'CWE126':
        data.y = torch.tensor(cwe_dic['CWE126'])
    elif label == 0 and cwe == 'CWE127':
        data.y = torch.tensor(cwe_dic['CWE127'])
    elif label == 0 and cwe == 'CWE190':
        data.y = torch.tensor(cwe_dic['CWE190'])
    elif label == 0 and cwe == 'CWE401':
        data.y = torch.tensor(cwe_dic['CWE401'])
    else:
        print("error: no match CWE")
    return data


def dsm2data(file):
    model_path = r'D:\Desktop\hybrid-SVD\w2v_token\model_out\w2v_multi.model'
    w2vmodel = gensim.models.Word2Vec.load(model_path)
    data = []
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines()):
            vec = instruction2vec_(line, w2vmodel)
            data.append(vec)
    data = torch.tensor(np.array(data), dtype=torch.float)
    return data


def load_file(path_dot_dir, path_dsm_dir):
    dot_list = os.listdir(path_dot_dir)
    dsm_list = os.listdir(path_dsm_dir)

    if len(dsm_list) == len(dot_list):
        len_of_list = len(dsm_list)
    else:
        print("The len of dot files and dsm files is not equal!!! error!!!")
        sys.exit()

    for i in range(0, len_of_list):
        file_dot = os.path.join(path_dot_dir, dot_list[i])
        file_dsm = os.path.join(path_dsm_dir, dsm_list[i])
        yield file_dot, file_dsm


# 1: good    0: bad
def gendata():
    dataset = []
    path_base = r"D:\Desktop\hybrid-SVD\datasrc"
    for cwe in os.listdir(path_base):
        print("===>loading data from :", path_base + "\\" + cwe)
        path = os.path.join(path_base, cwe)
        path0 = path + r'\badres'
        path1 = path + r'\goodres'
        path0_dot = path0 + r'\dot'
        path0_dsm = path0 + r'\dsm_extract'
        path1_dot = path1 + r'\dot'
        path1_dsm = path1 + r'\dsm_extract'

        for f_dot, f_dsm in load_file(path0_dot, path0_dsm):
            dot = pydot.graph_from_dot_file(f_dot)
            data_dot = dot2data(dot, cwe, 0)
            data_dsm = dsm2data(f_dsm)
            data = [data_dot, data_dsm]
            if data != -1:
                dataset.append(data)

        for f_dot, f_dsm in load_file(path1_dot, path1_dsm):
            dot = pydot.graph_from_dot_file(f_dot)
            data_dot = dot2data(dot, cwe, 1)
            data_dsm = dsm2data(f_dsm)
            data = [data_dot, data_dsm]
            if data != -1:
                dataset.append(data)

    return dataset


if __name__ == "__main__":
    Dataset = gendata()
    random.shuffle(Dataset)
    # sum = 12872,
    # train: 2560 * 4 == 10240,
    # test : 12872-10240=2632 -> keep 2624
    for i_ in range(0, 4):
        with open(rf'D:\Desktop\hybrid-SVD\dataset\multi_train{i_}.pk', 'wb') as f_:
            pickle.dump(Dataset[i_*2560: (i_+1)*2560], f_)
    with open(rf'D:\Desktop\hybrid-SVD\dataset\multi_test.pk', 'wb') as f_:
        pickle.dump(Dataset[4 * 2560: 4 * 2560 + 2624], f_)

# if __name__ == "__main__":
#     h = []
#     for i_ in range(0, 4):
#         with open(rf'D:\Desktop\hybrid-SVD\dataset\multi_train{i_}.pk', 'rb') as f_:
#             cur_dataset = pickle.load(f_)
#             random.shuffle(cur_dataset)
#             for d in cur_dataset:
#                 h.append(len(d[1]))
#             del cur_dataset
#     with open(r'D:\Desktop\hybrid-SVD\dataset\multi_test.pk', 'rb') as f_:
#         cur_dataset = pickle.load(f_)
#         random.shuffle(cur_dataset)
#         for d in cur_dataset:
#             h.append(len(d[1]))
#         del cur_dataset
#     # define size of h of dsm
#     height_list = []
#     plt.hist(h)
#     plt.show()
