# coding=utf-8
import os

# 遍历路径path，删除名字为 name的文件／文件夹
def rmFilesInPath(path, name, isFile):
	"traverse folder:path, and remove the file named:name"
	print path, name, isFile
	curr_path = os.getcwd();
	# cd path
	os.chdir(path);
	print os.getcwd();
	if isFile == True:
		os.system("rm %s" % name)
	else:
		os.system("rm -rf %s" % name)
	# resume path
	os.chdir(curr_path)
	# traverse the path
	for dir in os.listdir(path):
		absolute_path = "%s/%s" % (path, dir)
		if os.path.isdir(absolute_path):
			rmFileInPath(absolute_path,name,isFile)

#rmFilesInPath(r"/Users/admin/Desktop/res", "cars*", True)