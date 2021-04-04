import numpy as np
import math
import json

class SimilarityClass:
    def __init__(self, SelectedFeature, geometryValueList):

        geometryNormalize = self.dataNormalize(geometryValueList)
        self.geometryValueList = np.copy(geometryNormalize)
        self.geometryValueList = self.geometryValueList.T

        self.SelectedFeature = SelectedFeature
        self.SbkValueList = self.GetSbkGeometry(self.SelectedFeature)


    def GetSbkGeometry(self, SelectedFeature):
        yzLine = json.loads(SelectedFeature["profile"])
        yzLine = self.dataNormalize(yzLine)

        sbkvalue = np.copy(yzLine)
        return sbkvalue.T


    def SimilarityCompare(self):
        dis = frechetDist(list(self.geometryValueList), list(self.SbkValueList))
        return dis


    def dataNormalize(self , valueList:list)-> list:#valueList =[[x,y] , [x,y]]
        temptXList=[]
        temptYList=[]

        # translate value from [x,y] format to [x1....xn],[y1....yn]
        for value in valueList:
            try:
                temptXList.append(float(value[0]))
                temptYList.append(float(value[1]))
            except:
                pass
        
        # general valueList
        # make the centerX=0
        meanX = (max(temptXList) + min(temptXList))/2
        for index in range(0,len(valueList)):
            temptXList[index] = temptXList[index] - meanX

        return [temptXList , temptYList] #return = [[x1...xn] , [y1....yn]]
    
"""

frechet distance

"""
# Euclidean distance.
def euc_dist(pt1,pt2):
    return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))


def _c(ca,i,j,P,Q):
    if ca[i,j] > -1:
        return ca[i,j]
    elif i == 0 and j == 0:
        ca[i,j] = euc_dist(P[0],Q[0])
    elif i > 0 and j == 0:
        ca[i,j] = max(_c(ca,i-1,0,P,Q),euc_dist(P[i],Q[0]))
    elif i == 0 and j > 0:
        ca[i,j] = max(_c(ca,0,j-1,P,Q),euc_dist(P[0],Q[j]))
    elif i > 0 and j > 0:
        ca[i,j] = max(min(_c(ca,i-1,j,P,Q),_c(ca,i-1,j-1,P,Q),_c(ca,i,j-1,P,Q)),euc_dist(P[i],Q[j]))
    else:
        ca[i,j] = float("inf")
    return ca[i,j]


def frechetDist(P,Q):
    ca = np.ones((len(P),len(Q)))
    ca = np.multiply(ca,-1)
    return _c(ca,len(P)-1,len(Q)-1,P,Q)