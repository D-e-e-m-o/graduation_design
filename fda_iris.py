#!/usr/bin/env python3

import numpy as np


def getData(dataFile):
	file = open(dataFile, 'r')
	try:
		data = []
		classes = {}
		for line in file.readlines():
			if line != '\n':
				dataTmp = [float(i) for i in line.split(',')[:4]]
				data.append(dataTmp)
				tmp = line.split(',')[-1]
				if not tmp in classes:
					classes[tmp] = [dataTmp]
				else:
					classes[tmp].append(dataTmp)
				# data = np.asarray(data, dtype='float')
	finally:
		file.close()
	nl = len(data)
	return data, classes, nl


def getW(data, classes, nl):
	# 求权值矩阵Wb和Ww
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
					tmpWb[-1].append(1 / nl - 1 / nk)
					tmpWw[-1].append(1 / nk)
				else:
					tmpWb[-1].append(1 / nl)
					tmpWw[-1].append(0)
		Wb[cl] = np.asarray(tmpWb)
		Ww[cl] = np.asarray(tmpWw)
	return Wb, Ww


def getS(data, Wb, Ww, nl):
	Sb = {}
	Sw = {}
	x = np.asarray(data)
	length = x[0].shape[0]
	for category in Wb.keys():
		Sb[category] = np.zeros([4, 4], dtype='float')
		Sw[category] = np.zeros([4, 4], dtype='float')
		for i in range(nl):
			for j in range(nl):
				tmp = (x[i] - x[j]).reshape(length, 1)
				Sb[category] += Wb[category][i][j] * tmp * tmp.T
				Sw[category] += Ww[category][i][j] * np.dot(tmp, tmp.T)
		Sb[category] *= 0.5
		Sw[category] *= 0.5
	return Sb, Sw


if __name__ == '__main__':
	dataFile = 'iris.data'
	data, classes, nl = getData(dataFile)
	Wb, Ww = getW(data, classes, nl)
	Sb, Sw = getS(data, Wb, Ww, nl)
	np.set_printoptions(threshold=np.NaN)
	fileWb = open('sb', mode='w')
	fileWw = open('sw', mode='w')
	try:
		fileWb.write(str(Sb))
		fileWw.write(str(Sw))
	finally:
		fileWb.close()
		fileWw.close()
