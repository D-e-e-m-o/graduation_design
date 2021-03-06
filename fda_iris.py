#!/usr/bin/env python3

import numpy as np
import itertools
import matplotlib.pyplot as plt


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
	return Sb, Sw


def dimReduction(Sb, Sw, data):
	V = data.shape[1]
	eigVals, eigVecs = np.linalg.eig(np.linalg.inv(Sw).dot(Sb))
	eig_pairs = [(np.abs(eigVals[i]), eigVecs[:, i]) for i in range(len(eigVals))]
	eig_pairs = sorted(eig_pairs, key=lambda k: k[0], reverse=True)
	Wa = np.hstack((eig_pairs[0][1].reshape(V, 1), eig_pairs[1][1].reshape(V, 1)))
	try:
		dataLda = data.dot(Wa)
	except AttributeError:
		dataLda = np.asarray(data, dtype='float').dot(Wa)
	return Wa, dataLda


def judge(vector, classes, Wa, Sw):
	numClasses = len(classes)
	V = vector.shape[0]
	aveClass = {}
	maxgj = -99999999
	solve = "not found"
	vector.reshape([1, V])
	for category in classes.keys():
		aveClass[category] = np.mean(classes[category], axis=0).reshape([1, V])
		nj = len(classes[category])
		gj = -0.5*(vector - aveClass[category]).dot(Wa)\
			.dot(np.linalg.inv(1 / (nj - 1)*Wa.T.dot(Sw[category]).dot(Wa)))\
			.dot(Wa.T).dot((vector - aveClass[category]).T)\
			- 0.5 * np.log(np.linalg.det(1 / (nj - 1) * Wa.T.dot(Sw[category]).dot(Wa)))
		if gj[0][0] > maxgj:
			maxgj = gj
			solve = category
	return solve


if __name__ == '__main__':
	dataFile = 'iris.data.bak'
	testFile = 'iris.data.bak'
	data, classes, nl = getData(dataFile)
	Ww = getW(data, classes, nl)
	Sb, Sw = getS(data, classes, Ww, nl)
	np.set_printoptions(threshold=np.NaN)
	fileSb = open('sb', mode='w')
	fileSw = open('sw', mode='w')
	Wa, dataLda = dimReduction(Sb, Sw['sum'], data)
	test, a, b = getData(testFile)
	print(dataLda)
	"""
	for i in itertools.chain(range(10), range(50, 65), range(100, 120)):
		vector = np.asarray(test[i], dtype='float')
		print(i+1, ':', judge(vector, classes, Wa, Sw)[:-1])
	"""
	plt.plot(dataLda[0:50][:, 0], dataLda[0:50][:, 1], 'r--',
				dataLda[50:100][:, 0], dataLda[50:100][:, 1], 'bs',
				dataLda[100:150][:, 0], dataLda[100:150][:, 1], 'g^')
	plt.show()
	try:
		fileSb.write(str(Sb))
		fileSw.write(str(Sw['sum']))
	finally:
		fileSb.close()
		fileSw.close()
