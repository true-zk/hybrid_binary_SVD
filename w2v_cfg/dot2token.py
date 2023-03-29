# trans dot files 2 token.txt
# input : path - path of the dot files
# input : out_file - the output file name
import os
import re
import pydot


# def loadfile(dotfile_dir_path):
#     for root, dirs, files in os.walk(dotfile_dir_path):
#         for dotfile in files:
#             dotfile = os.path.join(root, dotfile)
#             suffix = os.path.splitext(dotfile)[1]  # 后缀
#             if suffix == '.dot':
#                 try:
#                     yield dotfile
#                 except Exception as e:
#                     print(e)


def tokengen(node0):
    replace_dict = {
        r"\l": " ",
        "\"": " ",
        ",": " , ",
        ":": " ",
        "(": " ( ",
        ")": " ) ",
        "[": " [ ",
        "]": " ] ",
        "{": " { ",
        "}": " } ",
        "...": " "
    }
    for key in replace_dict:
        node0 = node0.replace(key, replace_dict[key])
    after_replace = node0.lower()
    sentences = []
    for word in after_replace.split():
        if re.match("^@.*(good|bad)", word):
            sentences.append("@func")
        else:
            sentences.append(word)
    return sentences


def output(token_list0, out_file_name):
    path_out = r'D:\Desktop\hybrid-SVD\w2v_cfg\token_out' + '\\' + out_file_name

    f = open(path_out, 'a')
    for token in token_list0:
        f.write(token + '\n')
    f.close()


def dot2token(path, out_file):
    for file in os.listdir(path):
        file = os.path.join(path, file)
        dot = pydot.graph_from_dot_file(file)
        nodes = dot[0].get_nodes()
        # nodes = nodes[1:]  # 第一个节点是shape = record 没有label
        if nodes is not None:
            for node in nodes:
                if not ('label' in node.obj_dict['attributes']):
                    continue
                node = node.obj_dict['attributes']['label']
                token_list = tokengen(node)
                output(token_list, out_file)


# if __name__ == '__main__':
#     path0 = r'D:\Desktop\hybrid-SVD\CWE23_good\dot'
#     path1 = r'D:\Desktop\hybrid-SVD\CWE23_bad\dot'
#     dot2token(path0)
#     dot2token(path1)



