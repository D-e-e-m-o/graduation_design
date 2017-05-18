#!/usr/bin/env python3

import numpy as np
import scipy.io as scio
import fda_iris as fda
import matplotlib.pyplot as plt


def getMatData(dataFile):
	file = scio.loadmat(dataFile)
	data = file['X'][:30]
	nl = len(data)
	# data, ave, std, p, dim = fda.pca(data, 0.9)
	ave = np.mean(data, axis=0)
	std = np.std(data, axis=0)
	data = (data - ave)/std
	dim = 13
	classes = {1: np.zeros(dim), 2: np.zeros(dim), 3: np.zeros(dim)}
	for i, j in zip(file['Y'][:30], data):
		classes[i[0]] = np.row_stack((classes[i[0]], j))
	classes[1] = np.delete(classes[1], 0, 0)
	classes[2] = np.delete(classes[2], 0, 0)
	classes[3] = np.delete(classes[3], 0, 0)
	y1 = file['Y'][:30]
	return data, classes, nl, y1, ave, std


def getMatTestData(dataFile, ave, std, dim=13):
	file = scio.loadmat(dataFile)
	data = file['X'][30:]
	data = (data - ave) / std
	classes = {1: np.zeros(dim), 2: np.zeros(dim), 3: np.zeros(dim)}
	for i, j in zip(file['Y'][30:], data):
		classes[i[0]] = np.row_stack((classes[i[0]], j))
	classes[1] = np.delete(classes[1], 0, 0)
	classes[2] = np.delete(classes[2], 0, 0)
	classes[3] = np.delete(classes[3], 0, 0)
	y1 = file['Y'][30:]
	return data, classes, y1


def getW(classes, y1, nl):
	# 求权值矩阵Ww
	Ww = {}
	tmpClasses = [i for i in classes]
	for cl in tmpClasses:
		tmpWw = []
		nk = len(classes[cl])
		for i in range(nl):
			tmpWw.append([])
			for j in range(nl):
				if y1[i] == cl and y1[j] == cl:
					tmpWw[-1].append(1 / nk)
				else:
					tmpWw[-1].append(0)
		Ww[cl] = np.asarray(tmpWw)
	return Ww


if __name__ == '__main__':
	dataFile = 'wine.mat'
	data, classes, nl, y1, ave, std = getMatData(dataFile)
	Ww = getW(classes, y1, nl)
	Sb, Sw = fda.getS(data, classes, Ww, nl)
	np.set_printoptions(threshold=np.NaN)
	fileSb = open('wine/sb', mode='w')
	fileSw = open('wine/sw', mode='w')
	fileWa = open('wine/wa', mode='w')
	fileData = open('wine/data', mode='w')
	fileClasses = open('wine/classes', mode='w')
	fileDataLda = open('wine/dataLda', mode='w')
	# testFile = 'corrected'
	try:
		fileSb.write(str(Sb))
		fileSw.write(str(Sw))
		Wa, dataLda = fda.dimReduction(Sb, Sw['sum'], data)
		# print(dataLda)
		fileWa.write(str(Wa))
		fileDataLda.write(str(dataLda))
		fileData.write(str(data))
		fileClasses.write(str(classes))
		yes = 0
		no = 0
		for i, j in zip(y1, dataLda):
			if i == 1:
				plt.plot(j[0], j[1], 'ro')
			elif i == 2:
				plt.plot(j[0], j[1], 'g^')
			else:
				plt.plot(j[0], j[1], 'b^')
		plt.savefig('wine/testfda.png')
		testData, testClasses, y2 = getMatTestData(dataFile, ave, std)
		for i, j in zip(testData, y2):
			solve = fda.judge(i, testClasses, Wa, Sw)
			if solve == j:
				yes += 1
			else:
				no += 1
		print(yes, no)
		print(yes / (yes + no))
	
	finally:
		fileSb.close()
		fileSw.close()
		fileWa.close()
		fileDataLda.close()
		fileData.close()
		fileClasses.close()
