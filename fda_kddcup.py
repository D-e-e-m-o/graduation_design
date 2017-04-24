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


def getData(dataFile):
	file = open(dataFile, 'r')
	line1 = ['tcp', 'udp', 'icmp']
	line2 = ['http', 'smtp', 'finger', 'domain_u', 'auth', 'telnet', 'ftp', 'eco_i', 'ntp_u', 'ecr_i', 'other', 'private', 'pop_3', 'ftp_data', 'rje', 'time', 'mtp', 'link', 'remote_job', 'gopher', 'ssh', 'name', 'whois', 'domain', 'login', 'imap4', 'daytime', 'ctf', 'nntp', 'shell', 'IRC', 'nnsp', 'http_443', 'exec', 'printer', 'efs', 'courier', 'uucp', 'klogin', 'kshell', 'echo', 'discard', 'systat', 'supdup', 'iso_tsap', 'hostnames', 'csnet_ns', 'pop_2', 'sunrpc', 'uucp_path', 'netbios_ns', 'netbios_ssn', 'netbios_dgm', 'sql_net', 'vmnet', 'bgp', 'Z39_50', 'ldap', 'netstat', 'urh_i', 'X11', 'urp_i', 'pm_dump', 'tftp_u', 'tim_i', 'red_i']
	line3 = ['SF', 'S1', 'REJ', 'S2', 'S0', 'S3', 'RSTO', 'RSTR', 'RSTOS0', 'OTH', 'SH']
	try:
		data = []
		classes = {'normal': [], 'bad': []}
		for i in range(300):
			line = file.readline()
			if line != '\n':
				tmp = line.split(',')
				dataTmp = [line1.index(tmp[1])+1, line2.index(tmp[2])+1, line3.index(tmp[3])+1,\
							float(tmp[4]), float(tmp[5])]
				data.append(dataTmp)
				if tmp[-1][:-2] == 'normal':
					classes['normal'].append(dataTmp)
				else:
					classes['bad'].append(dataTmp)
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
