#!/usr/bin/env python3
# 6 7 8 13 14 16-20 41
# tcp等等要编号映射
import fda_iris as fda
import numpy as np


def getData(dataFile):
	file = open(dataFile, 'r')
	try:
		data = []
		classes = {}
		for i in range(10000):
			line = file.readline()
			if line != '\n':
				dataTmp = [float(i) for i in line.split(',')[4:6]]
				data.append(dataTmp)
				tmp = line.split(',')[-1][:-2]
				if not tmp in classes:
					classes[tmp] = [dataTmp]
				else:
					classes[tmp].append(dataTmp)
				# data = np.asarray(data, dtype='float')
	finally:
		file.close()
	nl = len(data)
	return data, classes, nl


if __name__ == '__main__':
	dataFile = 'kddcup.data_10_percent'
	data, classes, nl = getData(dataFile)
	Ww = fda.getW(data, classes, nl)
	Sb, Sw = fda.getS(data, classes, Ww, nl)
	np.set_printoptions(threshold=np.NaN)
	fileWb = open('sb', mode='w')
	fileWw = open('sw', mode='w')
	fileWa = open('wa', mode='w')
	try:
		fileWb.write(str(Sb))
		fileWw.write(str(Sw['sum']))
		Wa, dataLda = fda.dimReduction(Sb, Sw['sum'], data)
		print(Wa)
		fileWa.write(str(Wa))
	finally:
		fileWb.close()
		fileWw.close()
		fileWa.close()
