###############################################################################
# hybrid model :
# __init__(self, size0, size1, labels)
# forward(x, edge_index, batch, t)
# 多分类
###############################################################################
import torch
import torch.nn as nn
from torch.nn import Linear, ReLU
import torch.nn.functional as F
from torch_geometric.nn import MessagePassing, TopKPooling
from torch_geometric.nn import global_mean_pool, global_max_pool
from torch_geometric.utils import degree
import math


# GCN layer
# cite: https://pytorch-geometric.readthedocs.io/en/latest/notes/create_gnn.html
class GCNConv(MessagePassing):
	def __init__(self, in_channels, out_channels, **kwargs):
		super().__init__(aggr='add', **kwargs)  # "Add" aggregation (Step 5).
		self.in_channels = in_channels
		self.out_channels = out_channels
		self.lin = Linear(in_channels, out_channels)

	def forward(self, x, edge_index):
		# x[N, in_channels]
		# edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))
		x = self.lin(x)
		row, col = edge_index

		deg = degree(col, x.size(0), dtype=x.dtype)

		deg_inv_sqrt = deg.pow(-0.5)
		deg_inv_sqrt[deg_inv_sqrt == float('inf')] = 0
		norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]
		return self.propagate(edge_index, size=(x.size(0), x.size(0)), x=x, norm=norm)

	def message(self, x_j, norm):
		# x_j has shape [E, out_channels]

		# Step 4: Normalize node features.
		return norm.view(-1, 1) * x_j

	def update(self, aggr_out):
		# aggr_out has shape [N, out_channels]
		# Step 6: Return new node embeddings.
		return aggr_out


# Whole NN model
class HybridNet(torch.nn.Module):
	def __init__(self, size0, size1, labels):
		super(HybridNet, self).__init__()
		self.labels = labels
		###############################################################################
		# GCN model   																  #
		###############################################################################
		self.conv1 = GCNConv(256, 256)
		self.pool1 = TopKPooling(256, ratio=0.8)
		self.conv2 = GCNConv(256, 256)
		self.pool2 = TopKPooling(256, ratio=0.8)
		self.conv3 = GCNConv(256, 256)
		self.pool3 = TopKPooling(256, ratio=0.8)
		self.conv4 = GCNConv(256, 256)
		self.pool4 = TopKPooling(256, ratio=0.8)
		self.conv5 = GCNConv(256, 256)
		self.pool5 = TopKPooling(256, ratio=0.8)

		self.convAtt1 = torch.nn.Conv1d(in_channels=512, out_channels=64, kernel_size=1, stride=2)
		self.poolAtt1 = torch.nn.MaxPool1d(kernel_size=1, stride=2)
		self.convAtt2 = torch.nn.Conv1d(64, 16, kernel_size=1, stride=2)
		self.poolAtt2 = torch.nn.MaxPool1d(kernel_size=1, stride=2)
		self.convAtt3 = torch.nn.Conv1d(16, 2, kernel_size=1, stride=2)
		self.poolAtt3 = torch.nn.MaxPool1d(kernel_size=1, stride=2)

		self.convAtt4 = torch.nn.Conv1d(2, 16, kernel_size=1, stride=2)
		self.poolAtt4 = torch.nn.MaxPool1d(kernel_size=1, stride=2)
		self.convAtt5 = torch.nn.Conv1d(16, 64, kernel_size=1, stride=2)
		self.poolAtt5 = torch.nn.MaxPool1d(kernel_size=1, stride=2)
		self.convAtt6 = torch.nn.Conv1d(64, 512, kernel_size=1, stride=2)
		self.poolAtt6 = torch.nn.MaxPool1d(kernel_size=1, stride=2)

		###############################################################################
		# textCNN model   															  #
		###############################################################################
		h_input = size0
		w_input = size1
		filter_list = [2, 4, 6, 8, 10, 12, 16, 20]
		num_per_filter = 64
		h_raw = [h_input - i + 1 for i in filter_list]  # 175-filter_size+1: after conv
		filter_list1 = [math.ceil(i / 2) for i in h_raw]  # p = ceil[h_raw / 2]
		h_res = sum(h_raw)  # h of res
		self.num_filter = len(filter_list)
		self.conv_t = nn.ModuleList([nn.Conv2d(1, num_per_filter, (cnv_size, w_input)) for cnv_size in filter_list])
		self.max_t = nn.MaxPool2d(kernel_size=(num_per_filter, 1))
		self.avg_t = nn.AvgPool2d(kernel_size=(num_per_filter, 1))
		self.conv_t1 = nn.ModuleList([nn.Conv2d(2, 1, (cnv_size, 1), padding='same') for cnv_size in filter_list1])
		self.sig = nn.Sigmoid()

		###############################################################################
		# hybrid output   															  #
		###############################################################################
		h_res = sum(h_raw)  # textCNN_input_feature

		self.lin1 = torch.nn.Linear(512 + h_res, 512)
		self.lin2 = torch.nn.Linear(521, 128)
		self.lin3 = torch.nn.Linear(128, 64)
		self.lin4 = torch.nn.Linear(64, labels)
		self.dropout = nn.Dropout(0.6)

	def forward(self, x, edge_index, batch, t):
		###############################################################################
		# GCN model :  x, edge_index, batch = data.x, data.edge_index, data.batch	  #
		###############################################################################
		x = F.relu(self.conv1(x, edge_index))
		x, edge_index, _, batch, _, _ = self.pool1(x, edge_index, None, batch)
		x1 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

		x = F.relu(self.conv2(x, edge_index))
		x, edge_index, _, batch, _, _ = self.pool2(x, edge_index, None, batch)
		x2 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

		x = F.relu(self.conv3(x, edge_index))
		x, edge_index, _, batch, _, _ = self.pool3(x, edge_index, None, batch)
		x3 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

		x = F.relu(self.conv4(x, edge_index))
		x, edge_index, _, batch, _, _ = self.pool4(x, edge_index, None, batch)
		x4 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

		x = F.relu(self.conv5(x, edge_index))
		x, edge_index, _, batch, _, _ = self.pool5(x, edge_index, None, batch)
		x5 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

		x = x1 + x2 + x3 + x4 + x5

		x = 1 / 5 * x

		sx = x

		x = x.unsqueeze(dim=2)

		# attention
		x = F.relu(self.convAtt1(x))
		x = self.poolAtt1(x)
		x = F.relu(self.convAtt2(x))
		x = self.poolAtt2(x)
		x = F.relu(self.convAtt3(x))
		x = self.poolAtt3(x)

		x = F.relu(self.convAtt4(x))
		x = self.poolAtt4(x)
		x = F.relu(self.convAtt5(x))
		x = self.poolAtt5(x)
		x = F.relu(self.convAtt6(x))
		x = self.poolAtt6(x)
		x = x.squeeze()

		x = (x + 1) * sx

		###############################################################################
		# TextCNN model :  t = batch * h * w										  #
		###############################################################################
		t = torch.unsqueeze(t, 1)
		t = [torch.squeeze(F.relu(conv(t)), 3) for conv in self.conv_t]
		# per_filter * [batch * num_per_filter * h_raw]
		max_ = []
		avg_ = []
		for i in t:
			i = torch.unsqueeze(i, 1)
			max_.append(torch.unsqueeze(torch.squeeze(self.max_t(i), 1), 3))
			avg_.append(torch.unsqueeze(torch.squeeze(self.avg_t(i), 1), 3))

		for i in range(0, self.num_filter):
			attention_ = torch.cat((max_[i], avg_[i]), dim=1)
			attention_ = self.sig(self.conv_t1[i](attention_))
			attention_ = torch.unsqueeze(torch.squeeze(attention_, 3), 1)
			t[i] *= attention_
			t[i] = torch.squeeze(self.max_t(t[i]))
		t = torch.cat(t, dim=1)
		t = torch.squeeze(t)

		###############################################################################
		# hybrid output :  #
		###############################################################################
		# out layer
		x = torch.cat((x, t))  # 512 + 1000

		x = F.relu(self.lin1(x))
		x = F.dropout(x, p=0.5, training=self.training)
		x = F.relu(self.lin2(x))
		x = F.relu(self.lin3(x))
		x = F.log_softmax(self.lin4(x), dim=-1)

		return x
