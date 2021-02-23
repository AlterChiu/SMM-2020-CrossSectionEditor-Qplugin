import pyqtgraph as pyqtgraph
from pyqtgraph import PlotWidget, plot
from PyQt5 import QtCore
import traceback
import statistics


class PlotWidgetClass:
    def __init__(self, plotWidget: pyqtgraph.PlotWidget):
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
            "color": "black",
            "font-weight": "bold",
            "font-size": "16px",
        }
        self.__plotWidget.setLabel('left', "Level(m)", **self.__labelStyle)
        self.__plotWidget.setLabel(
            "bottom", "Distance(m)", **self.__labelStyle)

        # set line values
        # dataLine = [[[Vx1....Vxn] , [Vy1....Vyn] ], [[Wx1....Wxn],[Wy1....Wyn]].....]
        self.__data = {
            "primary": [],
            "seconds": [],
            "sbk": [],
            "fixPoint": {
                "dem": {
                    "right": [],  # [y,z]
                    "left": []  # [y,z]
                },
                "sbk": {
                    "rigth": [],  # [y,z]
                    "left": []  # [y,z]
                }
            }
        }

        self.__line = {
            "primary": None,
            "sbk": None,
            "fixPoint": {
                "dem": {
                    "right": None,
                    "left": None
                },
                "sbk": {
                    "right": None,
                    "left": None
                }
            }
        }

    # public functions
    # --------------------------------------------------------------------------------------

    def plot(self):
        self.plotSecondary()
        self.plotPrimary()
        self.plotSBK()

    def plotSBK(self):
        # SBK pen
        sbkPen = pyqtgraph.mkPen(color="b")

        # plot SBK line
        try:
            temptXList = self.__data["sbk"][0][0]
            temptYList = self.__data["sbk"][0][1]
            self.__line["sbk"] = self.__plotWidget.plot(
                temptXList, temptYList, pen=sbkPen)
        except:
            print("error plotSBK")

    def plotPrimary(self):
        # primary pen
        primaryPen = pyqtgraph.mkPen(color="r")

        # plot primary line
        try:
            temptXList = self.__data["primary"][0][0]
            temptYList = self.__data["primary"][0][1]
            self.__line["primary"] = self.__plotWidget.plot(
                temptXList, temptYList, pen=primaryPen)
        except:
            print("plot primary")

    def plotSecondary(self):
        # secondary pen
        secondPen = pyqtgraph.mkPen(color="g")

        # plot secondary lines
        for dataLine in self.__data["seconds"]:
            try:
                temptXList = dataLine[0]
                temptYList = dataLine[1]
                self.__plotWidget.plot(temptXList, temptYList, pen=secondPen)
            except:
                print("plot secondary")

    def plotFixPoints(self, prefixName: str):
        color = {
            "dem": "r",
            "sbk": "b"
        }
        fixPointPen = pyqtgraph.mkPen(color=color[prefixName])

        try:
            # plot left point
            self.__line["fixPoint"][prefixName]["left"] = self.__plotWidget.plot([self.__data["fixPoint"][prefixName]["left"][0]], [
                self.__data["fixPoint"][prefixName]["left"][1]], pen=fixPointPen, symbol="o", symbolSize=10, symbolBrush=(color[prefixName]))

            # plot left point
            self.__line["fixPoint"][prefixName]["right"] = self.__plotWidget.plot([self.__data["fixPoint"][prefixName]["right"][0]], [
                self.__data["fixPoint"][prefixName]["right"][1]], pen=fixPointPen, symbol="o", symbolSize=10, symbolBrush=(color[prefixName]))

        except:
            traceback.print_exc()
            print("plot FixPoint error " + prefixName)

    def rePlotPrimary(self, valueList: list):
        self.clearPrimaryLine()
        self.addDataPrimary(valueList)
        self.plotPrimary()

    def rePlotSBK(self, valueList: list):
        self.clearSbkLine()
        self.addDataSBK(valueList)
        self.plotSBK()

# data functions
# --------------------------------------------------------------------------------------
    # clear all data from dataLine collection and also clear plot
    def clear(self):
        self.clearFixPoint("sbk")
        self.clearFixPoint("dem")
        self.clearSbkLine()
        self.clearSecondary()
        self.clearPrimaryLine()
        
        self.__plotWidget.clear()

    def clearFixPoint(self , prefixName):
        rightLefts = ["right" , "left"]
        
        for rightLeft in rightLefts:
            try:
                self.__plotWidget.removeItem(
                    self.__line["fixPoint"][prefixName][rightLeft])
                self.__line["fixPoint"][prefixName][rightLeft].clear()
                self.__line["fixPoint"][prefixName][rightLeft] = None
                self.__data["fixPoint"][prefixName][rightLeft] = []
            except:
                pass
    
    def clearSecondary(self):
        try:
            self.__plotWidget.removeItem(self.__line["seconds"])
        except:
            print("no seconds data to clear")

        self.__line["seconds"] = None
        self.__data["seconds"].clear()       
    
    def clearSbkLine(self):
        try:
            self.__plotWidget.removeItem(self.__line["sbk"])
        except:
            print("no sbk data to clear")

        self.__line["sbk"] = None
        self.__data["sbk"].clear()

    def clearPrimaryLine(self):
        try:
            self.__plotWidget.removeItem(self.__line["primary"])
        except:
            pass

        self.__line["primary"] = None
        self.__data["primary"].clear()

    # valueList = [[x,y,z] , [x,y,z]]
    def addDataPrimary(self, valueList: list):
        self.__addData(valueList, self.__data["primary"])

    def addDataSBK(self, valueList: list):  # valueList = [[x,y] , [x,y]]
              
        # without data normalize
        temptXList = []
        temptYList = []

        for value in valueList:
            temptXList.append(value[0])
            temptYList.append(value[1])

        self.__data["sbk"].append([temptXList, temptYList])

    # valueList = [[y,z] , [y,z]]
    def addDataSecondary(self, valueList: list):
        self.__addData(valueList, self.__data["seconds"])

    # add one more data to dataLine collection
    # valueList = [[y,z] , [y,z]]
    def __addData(self, valueList: list, temptDataLine: list):
        # normalize data
        normalizeDatat = self.dataNormalize(valueList)

        # add to dataLine collections
        # valueList = [[[x1...xn] , [y1....yn]] , [[x1...xn],[y1...yn]]]
        # temptDataLine [[[x1...xn] , [y1.....yn]] , [[x1...xn] , [y1.....yn]]]
        temptDataLine.append(normalizeDatat)

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
        self.__plotWidget.setXRange(
            self.__labelMaxX, self.__labelMinX, padding=0)
        self.__plotWidget.setYRange(
            self.__labelMaxY, self.__labelMinY, padding=0)

    # valueList =[[x,y] , [x,y]]
    # return = [[x1...xn] , [y1....yn]]
    def dataNormalize(self, valueList: list) -> list:
        temptXList = []
        temptYList = []

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
        for index in range(0, len(valueList)):
            temptXList[index] = temptXList[index] - meanX

        return [temptXList, temptYList]  

    # set fixed point, refixName for [dem , sbk] , leftRight for [right,left]
    def setFixPoint(self, y: float, z: float, prefixName: str, leftRight: str) -> bool:

        try:
            translatedY = float(y)
            translatedZ = float(z)

            self.__data["fixPoint"][prefixName][leftRight] = [y, z]
            return True
        except:
            print("FixPoint convert exception " + prefixName + "_" + leftRight)
            return False
    # set title

    def setTitle(self, titleID=""):
        self.__plotWidget.setTitle(titleID)
