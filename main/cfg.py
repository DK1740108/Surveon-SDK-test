# Surveon SDK, AutoTest Plan.
# Dreizehn.Wei
# Fun(): cfg_get_file_keyword

import os, sys, time, webbrowser

def cfg_GetKey(filename, key, subkey):
	outData = ""
	findflag = 0
	file = open(filename, "r")
	for line in file.readlines():
		line = line.strip('\n')
		line = line.strip(' ')
		if findflag == 0:
			ret = line.find(key)
			if ret == 1:
				findflag = 1
		else:
			filedata = line.split("=")
			filedata[0] = filedata[0].strip('\n')
			filedata[0] = filedata[0].strip(' ')
			if cmp(filedata[0], subkey) == 0:
				outData = filedata[1].strip(' ')
				#print(output)
				break
	file.close()
	if findflag == 0:
		outData = "Unknown"
	return outData

def cfg_SetKey(filename, key, subkey, data):
	findflag = 0
	ifile = open(filename, "r")
	ofile = open(filename+".tmp", "w")
	for line in ifile.readlines():
		if findflag == 0:
			ofile.write(line)
			ret = line.find(key)
			if ret == 1:
				findflag = 1
		else:
			filedata = line.split("=")
			filedata[0] = filedata[0].strip('\n')
			filedata[0] = filedata[0].strip(' ')
			if cmp(filedata[0], subkey) == 0:
				ofile.write(filedata[0] + " = " + data + "\n")
				findflag = 0
			else:
				ofile.write(line)
	ifile.close()
	ofile.close()
	os.remove(filename)
	os.rename(filename+".tmp", filename)

