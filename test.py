#!/usr/bin/env python
from fda_kddcup import getMatData
import numpy as np
from fda_iris import pca

np.set_printoptions(threshold=np.NaN)
dataFile = 'KDD99data.mat'
data, classes, nl, y1 = getMatData(dataFile)
test = pca(data, 0.5)
print(test)
