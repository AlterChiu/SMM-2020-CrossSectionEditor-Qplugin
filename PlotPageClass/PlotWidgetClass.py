import pyqtgraph as pyqtgraph
from pyqtgraph import PlotWidget, plot
from PyQt5 import QtCore
import statistics

class PlotWidgetClass:
    def __init__(self , plotWidget: pyqtgraph.PlotWidget):
        self.__plotWidget = plotWidget

        self.__labelMaxX = 100
        self.__labelMinX = 0
        self.__labelMaxY = 10
        self.__labelMinY = -3

        # set background in white
        self.__plotWidget.setBackground("w")

        # set grid
        self.__plotWidget.showGrid(x=True, y=True)

        # set label
        self.__labelStyle = {
            "color" : "black",
            "font-weight":"bold",
            "font-size" : "16px",
        }
        self.__plotWidget.setLabel('left', "Level(m)", **self.__labelStyle)
        self.__plotWidget.setLabel("bottom" , "Distance(m)" , **self.__labelStyle)
        
        # set line values
        # dataLine = [[[Vx1....Vxn] , [Vy1....Vyn] ], [[Wx1....Wxn],[Wy1....Wyn]].....]
        self.__dataLineList = []
        self.__dataLinePrimary = []
        self.__dataLineSBK = []

        # plot line
        self.__primaryLine=None
        self.__sbkLine=None

    # public functions
    #--------------------------------------------------------------------------------------
    def plot(self):
        self.plotSecondary()
        self.plotPrimary()
        self.plotSBK()

    def plotSBK(self):
        # SBK pen
        sbkPen = pyqtgraph.mkPen(color="b")

        # plot SBK line
        try:
            temptXList = self.__dataLineSBK[0][0]
            temptYList = self.__dataLineSBK[0][1]
            self.__sbkLine = self.__plotWidget.plot(temptXList , temptYList ,pen = sbkPen)
        except:
            print("error plotSBK")

    def plotPrimary(self):
        # primary pen
        primaryPen = pyqtgraph.mkPen(color="r")

        # plot primary line
        try:
            temptXList = self.__dataLinePrimary[0][0]
            temptYList = self.__dataLinePrimary[0][1]
            self.__primaryLine = self.__plotWidget.plot(temptXList , temptYList ,pen = primaryPen)
        except:
            print("plot primary")

    def plotSecondary(self):
        # secondary pen
        secondPen = pyqtgraph.mkPen(color="g")

        # plot secondary lines
        for dataLine in self.__dataLineList:
            try:
                temptXList=dataLine[0]
                temptYList=dataLine[1]
                self.__plotWidget.plot(temptXList , temptYList ,pen = secondPen)
            except:
                print("plot secondary")

    def rePlotPrimary(self , valueList:list):
        self.clearPrimaryLine()
        self.addDataPrimary(valueList)
        self.plotPrimary()
    
    def rePlotSBK(self , valueList:list):
        self.clearSbkLine()
        self.addDataSBK(valueList)
        self.plotSBK()

# data functions
#--------------------------------------------------------------------------------------
    # clear all data from dataLine collection and also clear plot
    def clear(self):
        self.__dataLineList.clear()
        self.__dataLinePrimary.clear()
        self.__dataLineSBK.clear()
        self.__plotWidget.clear()
    
    def clearSbkLine(self):
        try:
            self.__sbkLine.clear()    
        except:
            print("no sbk data to clear")

        self.__sbkLine =None
        self.__dataLineSBK.clear()

    def clearPrimaryLine(self):
        try:
            self.__plotWidget.removeItem(self.__primaryLine)
            self.__primaryLine =None
        except:
            pass
        self.__dataLinePrimary=[]

    def addDataPrimary(self , valueList:list): #valueList = [[x,y] , [x,y]]
        self.__addData(valueList , self.__dataLinePrimary)

    def addDataSBK(self , valueList:list): #valueList = [[x,y] , [x,y]]
        # without data normalize
        temptXList = []
        temptYList = []

        for value in valueList:
            temptXList.append(value[0])
            temptYList.append(value[1])

        self.__dataLineSBK.append([temptXList , temptYList])
        
    def addDataSecondary(self , valueList:list):#valueList = [[x,y] , [x,y]]
        self.__addData(valueList , self.__dataLineList)

    # add one more data to dataLine collection
    def __addData(self , valueList:list , temptDataLine:list): #valueList = [[x,y] , [x,y]]
        # normalize data
        normalizeDatat = self.dataNormalize(valueList)

        # add to dataLine collections
        temptDataLine.append(normalizeDatat) #valueList = [[[x1...xn] , [y1....yn]] , [[x1...xn],[y1...yn]]]

        # reset plotWidget range
        try:
            temptMaxX = max(normalizeDatat[0])+1
            if temptMaxX > self.__labelMaxX:
                self.__labelMaxX = temptMaxX
        except:
            pass
        
        try:
            temptMinX = min(normalizeDatat[0])-1
            if self.__labelMinX > temptMinX:
                self.__labelMinX = temptMinX
        except:
            pass

        try:
            temptMaxY = max(normalizeDatat[1])+1
            if self.__labelMaxY < temptMaxY:
                self.__labelMaxY = temptMaxY
        except:
            pass

        try:
            temptMinY = min(normalizeDatat[1])-1
            if self.__labelMinY > temptMinY:
                self.__labelMinY = temptMinY
        except:
            pass

         # setRange
        self.__plotWidget.setXRange(self.__labelMaxX, self.__labelMinX, padding=0)
        self.__plotWidget.setYRange(self.__labelMaxY, self.__labelMinY, padding=0)

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
        meanX = statistics.mean(temptXList)
        for index in range(0,len(valueList)):
            temptXList[index] = temptXList[index] - meanX

        return [temptXList , temptYList] #return = [[x1...xn] , [y1....yn]]
    

    # set title
    def setTitle(self , titleID=""):
        self.__plotWidget.setTitle(titleID)



