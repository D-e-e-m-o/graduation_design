#!/usr/bin/env python3

import numpy as np


def getData(dataFile):
	file = open(dataFile, 'r')
	try:
		data = []
		classes = {}
		for line in file.readlines():
			if line != '\n':
				dataTmp = [float(i) for i in line.split(',')[1:]]
				data.append(dataTmp)
				tmp = line.split(',')[0]
				if not tmp in classes:
					classes[tmp] = [dataTmp]
				else:
					classes[tmp].append(dataTmp)
		# data = np.asarray(data, dtype='float')
	finally:
		file.close()
	return data, classes

def getW(data, classes):
	# 求权值矩阵Wb和Ww
	nl = len(data)
	Wb = {}
	Ww = {}
	tmpClasses = [i for i in classes.keys()]
	for cl in tmpClasses:
		tmpWb = []
		tmpWw = []
		nk = len(classes[cl])
		for i in range(nl):
			tmpWb.append([])
			tmpWw.append([])
			for j in range(nl):
				if (data[i] in classes[cl]) and (data[j] in classes[cl]):
					tmpWb[-1].append(1/nl-1/nk)
					tmpWw[-1].append(1/nk)
				else:
					tmpWb[-1].append(1/nl)
					tmpWw[-1].append(0)
		Wb[cl] = np.asarray(tmpWb)
		Ww[cl] = np.asarray(tmpWw)
	return Wb, Ww

if __name__ == '__main__':
	dataFile = 'wine.data'
	fileWb = open('wb', mode='w')
	fileWw = open('ww', mode='w')
	data, classes = getData(dataFile)
	Wb, Ww = getW(data, classes)
	np.set_printoptions(threshold=np.NaN)
	try:
		fileWb.write(str(Wb))
		fileWw.write(str(Ww))
	finally:
		fileWb.close()
		fileWw.close()
