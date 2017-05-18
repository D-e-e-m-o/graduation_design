#!/usr/bin/env python3

import numpy as np
import scipy.io as scio
import fda_iris as fda
from fda_kddcup import judge, getW


def getMatData(dataFile):
	file = scio.loadmat(dataFile)
	data = file['X'][:30]
	nl = len(data)
	data, ave, std, p, dim = fda.pca(data, 0.9)
	classes = {1: np.zeros(dim), 2: np.zeros(dim), 3: np.zeros(dim)}
	for i, j in zip(file['Y'][:30], data):
		classes[i[0]] = np.row_stack((classes[i[0]], j))
	classes[1] = np.delete(classes[1], 0, 0)
	classes[2] = np.delete(classes[2], 0, 0)
	classes[3] = np.delete(classes[3], 0, 0)
	y1 = file['Y'][:30]
	return data, classes, nl, y1, ave, std, p, dim


def getMatTestData(dataFile, ave, std, p, dim):
	file = scio.loadmat(dataFile)
	data = file['X'][30:]
	data = ((data - ave) / std).dot(p)
	classes = {1: np.zeros(dim), 2: np.zeros(dim), 3: np.zeros(dim)}
	for i, j in zip(file['Y'][30:], data):
		classes[i[0]] = np.row_stack((classes[i[0]], j))
	classes[1] = np.delete(classes[1], 0, 0)
	classes[2] = np.delete(classes[2], 0, 0)
	classes[3] = np.delete(classes[3], 0, 0)
	y1 = file['Y'][30:]
	return data, classes, y1


if __name__ == '__main__':
	dataFile = 'wine.mat'
	data, classes, nl, y1, ave, std, p, dim = getMatData(dataFile)
	print(nl)
	Ww, Wb = getW(data, classes, y1, nl)
	Sb, Sw = fda.getS(data, Ww, Wb, nl)
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
		Wa, dataLda = fda.dimReduction(Sb['sum'], Sw['sum'], data)
		# print(dataLda)
		fileWa.write(str(Wa))
		fileDataLda.write(str(dataLda))
		fileData.write(str(data))
		fileClasses.write(str(classes))
		yes = 0
		no = 0
		"""
		for i, j in zip(data, dataLda):
			if i in classes[0]:
				yes += 1
				# plt.plot(j[0], j[1], 'ro')
				pass
			else:
				no += 1
				# plt.plot(j[0], j[1], 'g^')
		# plt.savefig('kddcup/test400no.png')
		print(yes, no)
		"""
		testData, testClasses, y2 = getMatTestData(dataFile, ave, std, p, dim)
		for i, j in zip(testData, y2):
			solve = judge(i, testClasses, Wa, Sw)
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
