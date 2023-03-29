import re


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
