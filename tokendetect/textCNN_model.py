import pytorch_lightning as pl
import torch
from torch import nn
from torchmetrics.functional import accuracy

CLASSES = 2


class TextCNN(pl.LightningModule):
	def __init__(self):
		super().__init__()
		self.cnv = nn.Conv2d(1, 1, 5, 4)  # in channel, out channel, kernel, stride
		self.rel = nn.ReLU
		self.bn = nn.BatchNorm2d(1)
		self.max = nn.MaxPool2d(1)
		self.flat = nn.Flatten()
		self.fc1 = nn.Linear(128, 1)
		self.fc2 = nn.Linear(1, 1)
		self.fc3 = nn.Linear(1, CLASSES)
		self.softmax = nn.Softmax()
		self.accuracy = accuracy

	def forward(self, x):
		out = self.bn(self.rel(self.cnv(x)))
		out = self.flat(self.max(out))
		out = self.fc1(out)
		out = self.rel(out)
		out = self.fc2(out)
		out = self.rel(out)
		out = self.fc3(out)
		return out

	def loss_fn(self, out, target):
		return nn.CrossEntropyLoss()(out.view(-1, CLASSES), target)

	def configure_optimizers(self):
		LR = 1e-3
		optimizer = torch.optim.AdamW(self.parameters(), lr=LR)
		return optimizer

	def training_step(self, batch):
		x, y = batch["x"], batch["y"]
		out = self(x)
		loss = self.loss_fn(out, y)
		self.log("train_loss", loss)
		return loss

	def validation_step(self, batch):
		x, y = batch["x"], batch["y"]
		out = self(x)
		loss = self.loss_fn(out, y)
		out = nn.Softmax(-1)(out)
		logits = torch.argmax(out, dim=1)
		accu = self.accuracy(logits, y, task='binary')
		self.log("valid_loss", loss)
		self.log("train_acc_step", accu)
		return loss, accu
