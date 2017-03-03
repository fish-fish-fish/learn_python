#!/usr/bin/env python
# coding=utf-8
import re
# @property (nonatomic, weak, nullable) id <UITableViewDataSource> dataSource;
# @property (nonatomic, copy, nullable) UIColor *backgroundColor;
# - (void)tableView:(UITableView *)tableView willDisplayCell:(UITableViewCell *)cell forRowAtIndexPath:(NSIndexPath *)indexPath;
# - (CGFloat)tableView:(UITableView *)tableView heightForHeaderInSection:(NSInteger)section;

def formatPropertyLine(line):
	# 去除多余空白
	tmp = re.sub(r"\s+", " ", line)
	# 提取参数
	pattern = re.compile(r"(\s)*@(\s)*property(\s)*(\((?P<Propertys>[^\)]*)\))?(\s)*(?P<Type>[\w_]*)(\s)*(\<(?P<Delegate>[^\>]*)\>)?(\s)*(?P<Param>(\*)?(\s)*[^ ;]*);(\s)*(?P<Note>.*)")
	match = pattern.match(tmp)
	if match:
		values = match.groupdict()
		newline = "@property ("
		if values["Propertys"]:
			word = re.compile(r"[a-zA-Z]+")
			pl = re.findall(word, values["Propertys"])
			newline = newline + ", ".join(pl) + ")"
		newline = newline + values["Type"] + " "
		if values["Delegate"]:
			newline = newline + "<" + values["Delegate"] + "> "
		newline = newline + values["Param"].replace(" ","") + ";"
		if values["Note"]:
			note = values["Note"]
			getNote = re.compile(r"(\s)*//[/ ]*(?P<Text>.*)")
			res = getNote.match(note)
			if res and res.groupdict()["Text"]:
				note = res.groupdict()["Text"]
				newline = newline + " // " + note + "\n"
				return newline
			else:
				return newline + " "+ note + "\n"
		return newline
	else:
		return line

# - (CGFloat)tableView:(UITableView *)tableView heightForHeaderInSection:(NSInteger)section;
# 预处理：删除多余空白
# def preprocess(line:str) -> str:
def preprocess(line):
	tmp = re.sub(r"\s+"," ",line)
	return tmp;
# 提取方法类型
def getFuncType(line):
	return line.strip()[0]
# 提取返回值类型
def getReturnType(line):
	return_type = re.compile(r" ?[+-]{1} ?\((?P<TYPE>[^\)]+)\)")
	match = re.match(return_type, line)
	if match:
		return match.groupdict()["TYPE"].replace(" ","").replace("*", " *")
	else:
		return None

# 提取参数列表
def getVarList(line):
	pattern = None
	if line.count(":") == 0:
		return [(line.split(")")[1].split(";")[0].replace(";","").replace(" ", ""),),]
	else:
		pattern = re.compile(r" ?[\w_]+ ?: ?\( ?[\w_]+ ?\*? ?\) ?[\w_]+")
		coll = re.findall(pattern, line)
		res = []
		for var in coll:
			tmp = re.sub(r"\s+", "",var)
			pattern2 = re.compile(r"(?P<NAME>[^:]+):\((?P<TYPE>[^\)]+)\)(?P<VAR>.+)$")
			match2 = re.match(pattern2, tmp)
			if match2 and len(match2.groupdict()) == 3:
				res.append((match2.groupdict()["NAME"], match2.groupdict()["TYPE"], match2.groupdict()["VAR"]))
			else:
				return None
		return res
# 提取注释
def getNote(line):
	pattern = re.compile(r"[^;]+; ?(?P<NOTE>.*)$")
	match = re.match(pattern, line)
	if match:
		return match.groupdict()["NOTE"].replace(" ","").replace("//","// ")
	else:
		return None

def formatFuncDeclaration(line):
	# 去除空白
	tmp = preprocess(line)

	var_list = getVarList(tmp)
	print var_list
	if not (var_list and (len(var_list) > 1 or (len(var_list) == 1 and len(var_list[0]) == 1))):
		return line
	func_type = getFuncType(tmp)
	func_return_type = getReturnType(tmp)
	note = getNote(tmp)
	newline = func_type + " (" + func_return_type +  ")"
	for var in var_list:
		if len(var) == 1:
			newline = newline + var[0]
			break
		else:
			print var
			newline = newline + var[0] + ":(" + var[1] + ")" + var[2] + " "
	newline = newline.strip() + ";"
	if note:
		newline = newline + " " + note
	newline += "\n"
	return newline

# test
if __name__ == '__main__':
	pro1 = "@ property ( nonatomic	, copy, nullable)UIColor<deleagte> * backgroundColor; 		/* sss 	*/  \n"
	print pro1, formatPropertyLine(pro1)
	
	declear = "  - ( CGFloat* ) tableView  ; //  	xxxx\n"
	print declear, formatFuncDeclaration(declear)
	tu = (1,)
	print tu, len(tu)


