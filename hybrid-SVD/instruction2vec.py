# input a str(instruction); output a vec
import re
import numpy as np


Vecsize = 5


def replace_code(code):
	code = code.replace("imul rax, rax, 0x10", "imul rax, 0x10")  # 特殊处理
	code = code.replace("rep ", "rep")
	code = code.replace("repne ", "repne")
	code = code.replace(".byte", "")
	code = code.replace('dword ptr ', '')
	code = code.replace('dword dptr ', '')
	code = code.replace('qword ptr ', '')
	code = code.replace('byte ptr ', '')
	code = code.replace('word ptr ', '')
	code = code.replace("fs:", "")
	code = code.replace('[', '')
	code = code.replace(']', '')
	code = code.replace("- ", "-")
	code = code.replace("-", " -")
	code = code.replace("+", " ")
	code = re.sub(r"<.*>", '', code)
	return code


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
			print(operand_tmp, "more than 3 operand")
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
