import os
import re
import numpy as np
from util import replace_code
from gensim_w2v_model import Vecsize


def instruction2vec_(instruction, model):
	if not instruction:
		return 0
	instruction = replace_code(instruction)
	instruction_list = instruction.split()

	opcode = instruction_list[0]

	operand_str = instruction[len(opcode):]
	operand_list = operand_str.split(',')

	operand = [['0', '0', '0', '0'], ['0', '0', '0', '0']]

	for i, operand_tmp in enumerate(operand_list):
		operands = operand_tmp.split()
		if not operands:
			continue
		operand_list_tmp = ['0', '0', '0', '0']
		for operand0 in operands:
			if operand0[:2] == '0x' or operand0[:3] == '-0x':
				operand_list_tmp[1] = operand0
			elif re.match('[0-9]|-[0-9]', operand0):
				operand_list_tmp[3] = operand0
			elif len(operand0):
				if operand_list_tmp[0] == '0':
					operand_list_tmp[0] = operand0
				else:
					operand_list_tmp[2] = operand0
		if i >= 2:
			print(operand_tmp, "+++++++more than 2")
			continue
		operand[i] = operand_list_tmp
	zeros = np.zeros(Vecsize)

	ret_array = model.wv[opcode]
	for operands in operand:
		for operand0 in operands:
			if operand0 == '0':
				ret_array = np.hstack([ret_array, zeros])
			else:
				ret_array = np.hstack([ret_array, model.wv[operand0]])

	return ret_array


# if __name__ == '__main__':
# 	path = r'D:\Desktop\hybrid-SVD\datasrc\CWE23\CWE23_bad\dsm_extract\\'
# 	test_file = os.listdir(path)[3]
# 	print("test file :", test_file)
# 	model = gensim.models.Word2Vec.load(r".\w2vmodel\CWE23")
# 	with open(os.path.join(path, test_file), 'r') as f:
# 		lines = f.readlines()
# 		vec = instruction2vec_(lines[112], model, 5)
