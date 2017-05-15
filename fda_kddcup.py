#!/usr/bin/env python3
"""
6 7 8 13 14 16-20 41
tcp等等要编号映射
第一列--tcp:1,udp:2,icmp:3
第二列--['http', 'smtp', 'finger', 'domain_u', 'auth', 'telnet', 'ftp', 'eco_i', 'ntp_u', 'ecr_i', 'other', 'private', 'pop_3', 'ftp_data', 'rje', 'time', 'mtp', 'link', 'remote_job', 'gopher', 'ssh', 'name', 'whois', 'domain', 'login', 'imap4', 'daytime', 'ctf', 'nntp', 'shell', 'IRC', 'nnsp', 'http_443', 'exec', 'printer', 'efs', 'courier', 'uucp', 'klogin', 'kshell', 'echo', 'discard', 'systat', 'supdup', 'iso_tsap', 'hostnames', 'csnet_ns', 'pop_2', 'sunrpc', 'uucp_path', 'netbios_ns', 'netbios_ssn', 'netbios_dgm', 'sql_net', 'vmnet', 'bgp', 'Z39_50', 'ldap', 'netstat', 'urh_i', 'X11', 'urp_i', 'pm_dump', 'tftp_u', 'tim_i', 'red_i']
第三列--['SF', 'S1', 'REJ', 'S2', 'S0', 'S3', 'RSTO', 'RSTR', 'RSTOS0', 'OTH', 'SH']
"""
import fda_iris as fda
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio


def getW(data, classes, y1, nl):
	# 求权值矩阵Ww
	Ww = {}
	Wb = {}
	for cl in classes:
		tmpWw = []
		tmpWb = []
		nk = len(classes[cl])
		for i in range(nl):
			tmpWw.append([])
			tmpWb.append([])
			for j in range(nl):
				if (y1[i] == cl) and (y1[j] == cl):
					cigmai = 9999999
					cigmaj = cigmai
					for m in range(nl):
						if i != m:
							dist = np.linalg.norm(data[i] - data[m])
							if 0 < dist < cigmai:
								cigmai = dist
						if j != m:
							dist = np.linalg.norm(data[j] - data[m])
							if 0 < dist < cigmaj:
								cigmaj = dist
					Aij = np.exp(-(np.linalg.norm(data[i] - data[j]))**2 / cigmai / cigmaj)
					# Aij = 1
					tmpWw[-1].append(Aij / nk)
					tmpWb[-1].append(Aij * (1 / nl - 1 / nk))
				else:
					tmpWw[-1].append(0)
					tmpWb[-1].append(1 / nl)
		Ww[cl] = np.asarray(tmpWw)
		Wb[cl] = np.asarray(tmpWb)
	return Ww, Wb


def getTestData(dataFile):
	file = open(dataFile, 'r')
	line1 = ['tcp', 'udp', 'icmp']
	line2 = ['http', 'smtp', 'finger', 'domain_u', 'auth', 'telnet', 'ftp', 'eco_i', 'ntp_u', 'ecr_i', 'other', 'private', 'pop_3', 'ftp_data', 'rje', 'time', 'mtp', 'link', 'remote_job', 'gopher', 'ssh', 'name', 'whois', 'domain', 'login', 'imap4', 'daytime', 'ctf', 'nntp', 'shell', 'IRC', 'nnsp', 'http_443', 'exec', 'printer', 'efs', 'courier', 'uucp', 'klogin', 'kshell', 'echo', 'discard', 'systat', 'supdup', 'iso_tsap', 'hostnames', 'csnet_ns', 'pop_2', 'sunrpc', 'uucp_path', 'netbios_ns', 'netbios_ssn', 'netbios_dgm', 'sql_net', 'vmnet', 'bgp', 'Z39_50', 'ldap', 'netstat', 'urh_i', 'X11', 'urp_i', 'pm_dump', 'tftp_u', 'tim_i', 'red_i', 'icmp']
	line3 = ['SF', 'S1', 'REJ', 'S2', 'S0', 'S3', 'RSTO', 'RSTR', 'RSTOS0', 'OTH', 'SH']
	try:
		data = []
		classes = {'bad': []}
		for line in file.readlines():
			if line != '\n':
				tmp = line.split(',')
				dataTmp = [line1.index(tmp[1])+1, line2.index(tmp[2])+1, line3.index(tmp[3])+1,\
							float(tmp[4]), float(tmp[5])]
				if tmp[-1][:-2] not in classes:
					classes[tmp[-1][:-2]] = [dataTmp]
					data.append(dataTmp)
					if tmp[-1][:-2] != 'normal':
						classes['bad'].append(dataTmp)
				else:
					classes[tmp[-1][:-2]].append(dataTmp)
					data.append(dataTmp)
					if tmp[-1][:-2] != 'normal':
						classes['bad'].append(dataTmp)
				# data = np.asarray(data, dtype='float')
	finally:
		file.close()
	return data, {'normal': classes['normal'], 'bad': classes['bad']}


def getData(dataFile):
	file = open(dataFile, 'r')
	line1 = ['tcp', 'udp', 'icmp']
	line2 = ['http', 'smtp', 'finger', 'domain_u', 'auth', 'telnet', 'ftp', 'eco_i', 'ntp_u', 'ecr_i', 'other', 'private', 'pop_3', 'ftp_data', 'rje', 'time', 'mtp', 'link', 'remote_job', 'gopher', 'ssh', 'name', 'whois', 'domain', 'login', 'imap4', 'daytime', 'ctf', 'nntp', 'shell', 'IRC', 'nnsp', 'http_443', 'exec', 'printer', 'efs', 'courier', 'uucp', 'klogin', 'kshell', 'echo', 'discard', 'systat', 'supdup', 'iso_tsap', 'hostnames', 'csnet_ns', 'pop_2', 'sunrpc', 'uucp_path', 'netbios_ns', 'netbios_ssn', 'netbios_dgm', 'sql_net', 'vmnet', 'bgp', 'Z39_50', 'ldap', 'netstat', 'urh_i', 'X11', 'urp_i', 'pm_dump', 'tftp_u', 'tim_i', 'red_i', 'icmp']
	line3 = ['SF', 'S1', 'REJ', 'S2', 'S0', 'S3', 'RSTO', 'RSTR', 'RSTOS0', 'OTH', 'SH']
	try:
		data = []
		classes = {'bad': []}
		num = {}
		sum = 0
		for line in file.readlines():
			if line != '\n':
				tmp = line.split(',')
				dataTmp = [line1.index(tmp[1])+1, line2.index(tmp[2])+1, line3.index(tmp[3])+1,\
							float(tmp[4]), float(tmp[5])]
				if tmp[-1][:-2] not in classes:
					classes[tmp[-1][:-2]] = [dataTmp]
					data.append(dataTmp)
					sum += 1
					if tmp[-1][:-2] != 'normal':
						num[tmp[-1][:-2]] = 1
						classes['bad'].append(dataTmp)
					else:
						num[tmp[-1][:-2]] = 1
				elif num[tmp[-1][:-2]] <= 100:
					classes[tmp[-1][:-2]].append(dataTmp)
					data.append(dataTmp)
					num[tmp[-1][:-2]] += 1
					sum += 1
					if tmp[-1][:-2] != 'normal':
						classes['bad'].append(dataTmp)
			if sum >= 2300:
				break
				# data = np.asarray(data, dtype='float')
	finally:
		file.close()
	nl = len(data)
	return data, {'normal': classes['normal'], 'bad': classes['bad']}, nl


def getMatData(dataFile):
	file = scio.loadmat(dataFile)
	nl = len(file['x1'])
	data = np.delete(file['x1'], [6, 7, 14, 19, 20], 1)
	# ave = np.mean(data, axis=0)
	# std = np.std(data, axis=0)
	# data = (data - ave) / std
	classes = {0: np.zeros(36), 1: np.zeros(36), 2: np.zeros(36), 3: np.zeros(36)}
	for i, j in zip(file['y1'], data):
		classes[i[0]] = np.row_stack((classes[i[0]], j))
	classes[0] = np.delete(classes[0], 0, 0)
	classes[1] = np.delete(classes[1], 0, 0)
	classes[2] = np.delete(classes[2], 0, 0)
	classes[3] = np.delete(classes[3], 0, 0)
	y1 = file['y1']
	return data, classes, nl, y1


def getMatTestData(dataFile):
	file = scio.loadmat(dataFile)
	y2 = file['y2']
	data = np.delete(file['x2'], [6, 7, 14, 19, 20], 1)
	# ave = np.mean(data, axis=0)
	# std = np.std(data, axis=0)
	# data = (data - ave) / std
	classes = {0: np.zeros(36), 1: np.zeros(36), 2: np.zeros(36), 3: np.zeros(36)}
	for i, j in zip(file['y2'], data):
		classes[i[0]] = np.row_stack((classes[i[0]], j))
	classes[0] = np.delete(classes[0], 0, 0)
	classes[1] = np.delete(classes[1], 0, 0)
	classes[2] = np.delete(classes[2], 0, 0)
	classes[3] = np.delete(classes[3], 0, 0)
	return data, classes, y2


def judge(vector, classes, Wa, Sw):
	# numClasses = len(classes)
	aveClass = {}
	maxgj = -99999999
	solve = "not found"
	vector.reshape([1, len(vector)])
	for category in classes.keys():
		aveClass[category] = np.mean(classes[category], axis=0).reshape([1, len(vector)])
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
	# dataFile = 'kddcup.data_10_percent'
	np.set_printoptions(threshold=np.NaN)
	dataFile = 'KDD99data.mat'
	data, classes, nl, y1 = getMatData(dataFile)
	Ww, Wb = getW(data, classes, y1, nl)
	Sb, Sw = fda.getS(data, Ww, Wb, nl)
	fileSb = open('kddcup/sb', mode='w')
	fileSw = open('kddcup/sw', mode='w')
	fileWa = open('kddcup/wa', mode='w')
	fileData = open('kddcup/data', mode='w')
	fileClasses = open('kddcup/classes', mode='w')
	fileDataLda = open('kddcup/dataLda', mode='w')
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
		
		for i, j in zip(y1, dataLda):
			if i == 0:
				plt.plot(j[0], j[1], 'ro')
			elif i == 1:
				plt.plot(j[0], j[1], 'g^')
			elif i == 2:
				plt.plot(j[0], j[1], 'b^')
			else:
				plt.plot(j[0], j[1], 'c^')
		plt.savefig('kddcup/test400.png')
		
		testData, testClasses, y2 = getMatTestData(dataFile)
		for i, j in zip(testData, y2):
			# tmp = np.asarray(i, dtype='float')
			solve = judge(i, testClasses, Wa, Sw)
			if solve == j[0]:
					yes += 1
			else:
				no += 1
		print(yes, no)
		print(yes/(yes+no))
		
	finally:
		fileSb.close()
		fileSw.close()
		fileWa.close()
		fileDataLda.close()
		fileData.close()
		fileClasses.close()
