#!/sur/bin/env python
import splitDockMap
import numpy as np
import SOMTools
import sys

mapFileName = sys.argv[1]
gradThreshold = float(sys.argv[2])
nThreshold = int(sys.argv[3])
map = np.load(mapFileName)
uMatrix = np.load('uMatrix.npy')
outPath, clusterPathMat, grads = SOMTools.minPath(uMatrix, gradThreshold)
SOMTools.plotMat(clusterPathMat, 'clusterPathMat.pdf', interpolation='nearest')

mapCom_global, mapNorm1_global, mapNorm2_global, mapNorm3_global, mapVectors1_global,mapVectors2_global,mapVectors3_global = splitDockMap.splitMap(map,'global')

cIds = np.unique(clusterPathMat)
for i in cIds:
 sel = clusterPathMat==i
 n = sel.sum()
 if n > nThreshold:
  splitDockMap.get3Dvectors(mapCom_global[sel], mapVectors1_global[sel], mapNorm1_global[sel], 'global_c%s'%i)
