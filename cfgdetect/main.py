import gendata
import torch
from torch.nn import Sequential as Seq, Linear, ReLU
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import MessagePassing, TopKPooling
from torch_geometric.nn import global_mean_pool, global_max_pool
import random
import time
import numpy as np
import matplotlib.pyplot as plt

# start time log
time_start = time.time()

# load data -> Dataset
data_path_good = r"D:\Desktop\hybrid-SVD\CWE23_good\dot"
data_path_bad = r"D:\Desktop\hybrid-SVD\CWE23_bad\dot"

Dataset = gendata.gendata(data_path_good)
Dataset = Dataset + gendata.gendata(data_path_bad)

random.shuffle(Dataset)

lenDataset = len(Dataset)
len_Trainset = int(0.7 * lenDataset)
len_Validateset = int(0.2 * lenDataset)
len_Testset = lenDataset - len_Validateset - len_Trainset
Trainset = Dataset[:len_Trainset]
Validset = Dataset[len_Trainset: len_Validateset]
Testset = Dataset[len_Trainset + len_Validateset:]
print(f"len of dataset:{lenDataset}, \
        len of train:{len_Trainset}, \
        len of validate:{len_Validateset}, \
        len of test:{len_Testset}")

train_loader = DataLoader(Trainset, batch_size=32, shuffle=True)
test_loader = DataLoader(Testset, batch_size=32, shuffle=True)
good = 0
bad = 0
for test in Testset:
    if test["y"] == 1:
        good += 1
    else:
        bad += 1
print(f"good in testset:{good};;bad in testset:{bad}")

time_fin_load = time.time()
print("data load time: ", time_fin_load-time_start)