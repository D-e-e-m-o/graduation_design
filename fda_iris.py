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
	# 求权值矩阵Ww
	Ww = {}
	tmpClasses = [i for i in classes.keys()]
	for cl in tmpClasses:
		tmpWw = []
		nk = len(classes[cl])
		for i in range(nl):
			tmpWw.append([])
			for j in range(nl):
				if (data[i] in classes[cl]) and (data[j] in classes[cl]):
					tmpWw[-1].append(1 / nk)
				else:
					tmpWw[-1].append(0)
		Ww[cl] = np.asarray(tmpWw)
	return Ww


def getS(data, classes, Ww, nl):
	x = np.asarray(data)
	length = x[0].shape[0]
	Sb = np.zeros([length, length], dtype='float')
	Sw = {'sum': np.zeros([length, length], dtype='float')}
	aveClass = {}
	aveAll = np.mean(data, axis=0)
	for category in Ww.keys():
		aveClass[category] = np.mean(classes[category], axis=0)
		Sw[category] = np.zeros([length, length], dtype='float')
		for i in range(nl):
			for j in range(nl):
				tmp = (x[i] - x[j]).reshape(length, 1)
				Sw[category] += Ww[category][i][j] * np.dot(tmp, tmp.T)
		Sw[category] *= 0.5
		Sb += np.asarray(classes[category], dtype='float').shape[0] * \
				np.dot((aveClass[category] - aveAll).reshape(length, 1),
						(aveClass[category] - aveAll).reshape(1, length))
		Sw['sum'] += Sw[category]
	return Sb, Sw['sum']


if __name__ == '__main__':
	dataFile = 'iris.data'
	data, classes, nl = getData(dataFile)
	Ww = getW(data, classes, nl)
	Sb, Sw = getS(data, classes, Ww, nl)
	np.set_printoptions(threshold=np.NaN)
	fileWb = open('sb', mode='w')
	fileWw = open('sw', mode='w')
	try:
		fileWb.write(str(Sb))
		fileWw.write(str(Sw))
	finally:
		fileWb.close()
		fileWw.close()
