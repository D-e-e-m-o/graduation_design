#!/usr/bin/env python3

f = open('kddcup.data_10_percent','r')
#num = 0
dic = []
for l in f.readlines():
	t = l.split(',')[3]
	if t not in dic:
		dic.append(t)
print(dic)
