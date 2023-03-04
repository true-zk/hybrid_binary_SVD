import os
import re
import gensim
import pydot
import torch
import numpy as np
from torch_geometric.data import Data

w2vmodel = gensim.models.Word2Vec.load(r'D:\Desktop\hybrid-SVD\w2v\model_out\w2v256.model')


def gen_token(string: str):
    replace_dict = {"\l": " ",
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
    nodes = dot[0].get_nodes()
    edges = dot[0].get_edges()
    edge_list = []

    for node in nodes:
        if "label" not in node.obj_dict["attributes"]:
            index = nodes.index(node)
            print(f"\rdel === {index}")
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
    data.y = torch.tensor([label], dtype=torch.long)
    data.__setitem__('cwe', cwe)
    return data


def load_dot(path_dot_dir):
    cwe_pattern = re.compile(r'CWE[1-9]\d*')
    for file in os.listdir(path_dot_dir):
        file = os.path.join(path_dot_dir, file)
        try:
            cwe = str(cwe_pattern.search(file).group(0))
            if os.path.basename(file).find('good') != -1:
                label = 1
                yield file, cwe, label
            elif os.path.basename(file).find('bad') != -1:
                label = 0
                yield file, cwe, label
        except FileExistsError:
            print("error", file)
            continue


def gendata(path):
    dataset = []
    # k = 0
    for f, cwe, label in load_dot(path):
        dot = pydot.graph_from_dot_file(f)
        data = dot2data(dot, cwe, label)
        if data != -1:
            dataset.append(data)
        # k += 1
        # if k == 1:
        #     break
    return dataset


# if __name__ == '__main__':
#     data_path_good = r"D:\Desktop\hybrid-SVD\CWE23_good\dot"
#     data_path_bad = r"D:\Desktop\hybrid-SVD\CWE23_bad\dot"
#
#     Dataset = gendata(data_path_good)
#     from torch.nn import Sequential as Seq, Linear, ReLU
#     from torch_geometric.utils import add_self_loops, degree
#     x = Dataset[0].x
#     edge_index = Dataset[0].edge_index
#
#     edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))
#     lin = Linear(256, 256)
#     x = lin(x)
#     row, col = edge_index
#
#     print(x.size(0))
#
#     deg = degree(col, x.size(0), dtype=x.dtype)
#
#     print(deg)
#     print(edge_index)
