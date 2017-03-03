#!/usr/bin/env python
# coding=utf-8
import os
import sys
import re
# def isProperty(line:str) -> bool:
def isProperty(line):
	if line.strip().startswith(r"@property"):
		return True;
	else:
		return False;

# def isFuncDeclaration(line:str) -> bool:
def isFuncDeclaration(line):
	if (line.strip().startswith('+') or line.strip().startswith('-')) and line.strip().endswith(";"):
		return True;
	else:
		return False;

# def isFuncImplementation(line:str) -> bool:
def isFuncImplementation(line):
	if (line.strip().startswith("+") or line.strip().startswith("-")) and (not line.strip().endswith(";")):
		return True;
	else:
		return False;

# def isOCFile(filename:str) -> bool:
def isOCFile(filename):
	if filename.lower().strip().endswith(".m") or filename.lower().strip().endswith(".mm") or filename.lower().strip().endswith(".h"):
		return True;
	else:
		return False;

# def propertyIsLegal(propertyLine:str) -> bool:
def propertyIsLegal(propertyLine):
	pattern_property = re.compile(r"^@property \(((\w)+, )*((\w)*){1}\) (\w)* (\*)?(\w)+;")
	match = pattern_property.match(propertyLine)
	if match:
		return True;
	else:
		return False;

# def funcDeclarationIsLegal(functionLine:str) -> bool:
def funcDeclarationIsLegal(functionLine):
	pattern_function = re.compile(r"^[\-\+]{1} \((\w)+( \*)?\)(\w)+(:\((\w)+( \*)?\)(\w)+)?( (\w)+:\((\w)*( \*)?\)(\w)*)*;(\n)?")
	match = pattern_function.match(functionLine)
	if match:
		return True;
	else:
		return False;

# def funcImplementation(functionLine:str) -> bool:
def funcImplementationIsLegal(functionLine):
	pattern_function = re.compile(r"^[\-\+]{1} \((\w)+( \*)?\)(\w)+(:\((\w)+( \*)?\)(\w)+)?( (\w)+:\((\w)*( \*)?\)(\w)*)*(\s)*(\{)?(\s)*(\n)?")
	match = pattern_function.match(functionLine)
	if match:
		return True;
	else:
		return False;

# 检测指定路径中的oc文件，检测结果放入coll
# def checkFiels(path:str, coll:list):
def checkFiels(path, coll):
	oldPath = os.getcwd();
	os.chdir(path)
	for fileName in os.listdir(path):
		absPath = os.path.abspath(fileName)
		if os.path.isdir(absPath):
			checkFiels(absPath, coll)
		elif os.path.isfile(absPath) and isOCFile(fileName):
			fd = open(absPath, 'r')
			lineNo = 1
			for line in fd:
				if isFuncDeclaration(line) and not funcDeclarationIsLegal(line):
					coll.append(absPath + ":" + str(lineNo) + ":" + "funcDeclaration")
				elif isFuncImplementation(line) and not funcImplementationIsLegal(line):
					coll.append(absPath + ":" + str(lineNo) + ":" + "funcImplementation")
				elif isProperty(line) and not propertyIsLegal(line):
					coll.append(absPath + ":" + str(lineNo) + ":" + "property")
				lineNo += 1
			fd.close()
		else:
			continue;
	os.chdir(oldPath)

# 根据检测结果，生成表格
# def makeTable(coll:list md:str):
def makeTable(coll, outputFile):
	fd = open(outputFile,'w')
	fd.write(html_part1)
	index = 1
	for data in coll:
		items = str(data).split(":")
		row = r"<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (index, items[0], items[1], items[2])
		fd.write(row)
		index += 1
	fd.write(html_part2)
	fd.close()

# demo
html_part1 = '''<!DOCTYPE html>
<html>
<head>
<title>Format Report</title>
</head>
<body>
<h1>Format Report</h1>
<hr />
<h2>Summary</h2>
<table>
<thead>
<tr>
<th>No.</th><th>File Path</th><th>Line NO.</th><th>Type</th>
</tr>
</thead>
<tbody>
'''
html_part2 = '''
</tbody>
</table>
</body>
</html>
'''
if __name__ == '__main__':
	argc = len(sys.argv)
	print sys.argv,argc
	# check in path
	argv1 = "./"
	# output to path
	argv2 = "./"
	if argc >= 2:
		argv1 = sys.argv[1]
	if argc >= 3:
		argv2 = sys.argv[2]
	srcDir = os.path.abspath(argv1)
	outputFile = os.path.abspath(argv2) + "/result.html"
	print('''
		------------------------------------------------------------------------------------
		will check files in path: %s, 
		and the checking_result will write to file: %s
		------------------------------------------------------------------------------------
	''' % (srcDir, outputFile))
	coll = []
	checkFiels(srcDir, coll)
	makeTable(coll, outputFile)
	os.system("open %s" % outputFile)