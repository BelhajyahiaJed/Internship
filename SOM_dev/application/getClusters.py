#!/usr/bin/env python
import numpy as np
import SOMTools
from scipy import ndimage
import sys
import splitDockMap


def getClusters(map, uMatrix, relative_threshold):
 uMax = uMatrix.max()
 threshold = relative_threshold*uMax
 clusterMat = SOMTools.continuousMap(ndimage.label(uMatrix<threshold)[0])
 cIds = np.unique(clusterMat)[1:]
 uMeans = []
 uMins = []
 uMedians = []
 for i in cIds:
  sel = (clusterMat == i)
  uMean = uMatrix[sel].mean()
  uMin = uMatrix[sel].min()
  uMedian = np.median(uMatrix[sel])
  uMeans.append(uMean)
  uMins.append(uMin)
  uMedians.append(uMedian)
 sortedCids = cIds[np.argsort(uMeans)]
 sortedClusterMat = np.zeros_like(clusterMat)
# mapCom_global, mapNorm1_global, mapNorm2_global, mapNorm3_global, mapVectors1_global,mapVectors2_global,mapVectors3_global = splitDockMap.splitMap(map,'global')
 c = 0
 for i in sortedCids:
  c+=1
  sel = (clusterMat == i)
#  splitDockMap.get3Dvectors(mapCom_global[sel], mapVectors1_global[sel], mapNorm1_global[sel], 'global_c%s'%c)
  sortedClusterMat[sel] = c
  cId = np.where(cIds==i)[0][0]
  #update to print function
  print ('cId: %s, mean:%.2f, median: %.2f, min:%.2f'%(c, uMeans[cId], uMedians[cId], uMins[cId]))
  
 np.save('clusterMat.npy', sortedClusterMat)
 SOMTools.plotMat(sortedClusterMat, 'clusterMat.pdf', interpolation='nearest')
 return sortedClusterMat

def main():
 mapFileName = sys.argv[1]
 relative_threshold = float(sys.argv[2])
 map = np.load(mapFileName)
 uMatrix = np.load('uMatrix.npy')
 getClusters(map, uMatrix, relative_threshold)

if __name__ == '__main__':
 main()
