from PyQt5.QtWidgets import QTableWidget, QFrame, QAbstractItemView, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import statistics
import traceback
import sys
import math

from ..PlotPageClass import PlotWidgetClass


class TableWidgeClass:

    def __init__(self, tableWidget: QTableWidget, plotClass: PlotWidgetClass):
        # get plotClass
        self.__plotClass = plotClass

        # set table
        # ----------------------------
        self.__tableWidget = tableWidget
        self.__tableData = []  # [[x,y,l,z] , [x,y,l,z].....]

        # self.__tableWidget.horizontalHeader().setSectionResizeMode(5,QHeaderView.Stretch)# set 6 column autoSize
        self.__tableWidget.horizontalHeader().setSectionsClickable(
            False)  # unable click title

        # data
        # ----------------------------
        self.__startX = None
        self.__startY = None
        self.__startZ = None
        self.__endX = None
        self.__endY = None
        self.__endZ = None

        self.__totalLength = None

    # public functions
    # --------------------------------------------------------------
    def setStartPoint(self, x: float, y: float, z: float):
        self.__startX = None
        self.__startY = None
        self.__startZ = None
        self.__tableData.clear()
        self.__startX = x
        self.__startY = y
        self.__startZ = z

        try:
            deltX = self.__startX - self.__endX
            deltY = self.__startY - self.__endY
            self.__totalLength = math.sqrt(
                math.pow(deltX, 2) + math.pow(deltY, 2))
        except:
            pass

    def setEndPoint(self, x: float, y: float, z: float):
        self.__endX = None
        self.__endY = None
        self.__endZ = None
        self.__tableData.clear()
        self.__endX = x
        self.__endY = y
        self.__endZ = z

        try:
            deltX = self.__startX - self.__endX
            deltY = self.__startY - self.__endY
            self.__totalLength = math.sqrt(
                math.pow(deltX, 2) + math.pow(deltY, 2))
        except:
            pass

    def addPoint(self, l: float, z: float):
        try:
            # normalize y-z chart, which center y=0
            temptXY = self.__lengthToXY(l)
            temptX = temptXY[0]
            temptY = temptXY[1]

            # add to collection
            self.__tableData.append([temptX, temptY, l, z])
        except Exception:
            traceback.print_exc(file=sys.stdout)
            print("missing points:")
            print("startPoint: " + str(self.__startX) +
                  "\t" + str(self.__startY))
            print("endPoint: " + str(self.__endX) + "\t" + str(self.__endY))

    def deletPoint(self, index: int):
        try:
            self.__tableData.pop(index)
        except:
            pass

    def addNewRow(self):

        # disconnect
        try:
            self.__tableWidget.disconnect()
        except:
            pass

        self.addPoint(0, 0)
        newRow = self.__tableData[-1]
        self.__addLine(newRow[0], newRow[1], newRow[2], newRow[3])
        self.__tableWidget.scrollToBottom()

        # add onChange signal
        self.__tableWidget.cellChanged.connect(self.__reloadRow)

    def deletSelectedRow(self):
        selections = self.__tableWidget.selectionModel().selectedIndexes()
        for selection in selections:
            print(selection.row())
            self.deletPoint(selection.row())
        self.reload()

    def getTableValues(self) -> list:  # [[x,y,l,z]....]
        return self.__tableData

    def getStartPoint(self) -> list:  # [x,y,z]
        return [self.__startX, self.__startY, self.__startZ]

    def getEndPoint(self) -> list:  # [x,y,z]
        return [self.__endX, self.__endY, self.__endZ]

    # only operate after l,z edit
    # return [x,y]
    def setValue(self, row: int, column: int, value: float) -> list:
        try:
            self.__tableWidget.setItem(row, column, QTableWidgetItem(value))
            self.__reloadRow(row)
        except:
            print("table setValue caught error")
            pass

    # advace functions
    # ----------------------------------------------------------

    # valuelist = [[x,y,l,z]]

    def replace(self, valueList: list):
        # clear table data
        self.__tableData.clear()

        # set start end points
        self.setStartPoint(valueList[0][0], valueList[0][1], valueList[0][3])
        self.setEndPoint(valueList[-1][0], valueList[-1][1], valueList[-1][3])

        # add value to tables
        for point in valueList:
            self.__tableData.append(point)
        
        self.reload()

    # get middle L
    def __getLList(self) -> list:
        temptLList = []
        for point in self.__tableData:
            temptLList.append(point[2])
        return {
            "dataList": temptLList,
            "max": max(temptLList),
            "min": min(temptLList),
            "mid": (max(temptLList) + min(temptLList))/2
        }

    # get middle Z
    def __getZList(self) -> list:
        temptZList = []
        for point in self.__tableData:
            temptZList.append(point[3])
        return {
            "dataList": temptZList,
            "max": max(temptZList),
            "min": min(temptZList),
            "mid": (max(temptZList) + min(temptZList))/2
        }

    # move dateL , direction{ 0: bothSide , 1: rightSide , -1:leftSide}
    def __dataMoveL(self, direction: int, middleL: float):
        for row in range(0, len(self.__tableData)):
            temptL = self.__tableData[row][2]
            if direction == 0:
                temptL = self.__tableData[row][2] + moveL

            elif (self.__tableData[row][2]-middleL)*direction > 0:
                temptL = self.__tableData[row][2] + moveL

            temptXY = self.__lengthToXY(temptL)
            self.__tableData[row][0] = temptXY[0]
            self.__tableData[row][1] = temptXY[1]
            self.__tableData[row][2] = temptL

    # move dateZ , direction{ 0: bothSide , 1: topSide , -1:bottomSide}
    def __dataMoveZ(self, direction: int, middleZ: float):
        for row in range(0, len(self.__tableData)):
            temptZ = self.__tableData[row][3]

            if direction == 0:
                temptZ = self.__tableData[row][3] + moveZ

            elif (self.__tableData[row][3] - middleZ)*direction > 0:
                temptZ = self.__tableData[row][3] + moveZ

            self.__tableData[row][3] = temptZ

    # get limit L
    def __getLLimit(self, temptLList: dict, direction: int):
        if direction > 0:
            return {
                "rightLimit": temptLList["max"],
                "leftLimit": temptLList["mid"],
                "napPoint": temptLList["max"]
            }
        else:
            return {
                "rightLimit": temptLList["mid"],
                "leftLimit": temptLList["min"],
                "napPoint": temptLList["min"]
            }

    # get limit Z
    def __getZLimit(self, temptZList: dict, direction: int):
        if direction > 0:
            return {
                "topLimit": temptZList["max"],
                "bottomLimit": temptZList["mid"],
                "napPoint": temptZList["max"]
            }
        else:
            return {
                "topLimit": temptZList["mid"],
                "bottomLimit": temptZList["min"],
                "napPoint": temptZList["min"]
            }

    def __checkValue(self, lowerLimit: float, upperLimit: float, value: float):
        if value < lowerLimit:
            return lowerLimit
        elif value > upperLimit:
            return upperLimit
        else:
            return value

        # move => persantage to move
        # moveL = 1.05, which L will change from 1 to 1.05 (2 to 2.10), same as moveZ
        # direction <0:left , >0:right , 0: bothSide

    def dataMove(self, ratioL: float = 0.0, moveL: float = 0, directionL: int = 0, ratioZ: float = 0.0, moveZ: float = 0, directionZ: int = 0):

        # get middle L
        temptLList = self.__getLList()

        # get middle Z
        temptZList = self.__getZList()

        # get close to limit value
        for row in range(0, len(self.__tableData)):
            temptL = self.__tableData[row][2]
            temptZ = self.__tableData[row][3]

            # get which part to modified
            if (temptL - temptLList["mid"])*directionL >= 0 \
                    and (temptZ - temptZList["mid"])*directionZ >= 0:

                # get valueL , find limitValue , modify , check
                lLimit = self.__getLLimit(
                    temptLList, (temptL - temptLList["mid"]))
                temptL = temptL + moveL +\
                    (lLimit["napPoint"] - temptL) * ratioL

                if ratioL != 0:
                    temptL = self.__checkValue(
                        lLimit["leftLimit"], lLimit["rightLimit"], temptL)

                # get valueL , find limitValue , modify , check
                ZLimit = self.__getZLimit(
                    temptZList, (temptZ - temptZList["mid"]))
                temptZ = temptZ + moveZ +\
                    (ZLimit["napPoint"] - temptZ) * ratioZ

                if ratioZ != 0:
                    temptZ = self.__checkValue(
                        ZLimit["bottomLimit"], ZLimit["topLimit"], temptZ)

            temptXY = self.__lengthToXY(temptL)
            self.__tableData[row][0] = temptXY[0]
            self.__tableData[row][1] = temptXY[1]
            self.__tableData[row][2] = temptL
            self.__tableData[row][3] = temptZ

        self.reload()

    # private function
    # ----------------------------------------------------------
    def __addLine(self, x: float, y: float, l: float, z: float):
        row = self.__tableWidget.rowCount()
        self.__tableWidget.insertRow(row)

        temptXitem = QTableWidgetItem(str(x))
        temptYitem = QTableWidgetItem(str(y))
        temptLitem = QTableWidgetItem(str(l))
        temptZitem = QTableWidgetItem(str(z))

        self.__tableWidget.setItem(row, 0, temptXitem)
        self.__tableWidget.setItem(row, 1, temptYitem)
        self.__tableWidget.setItem(row, 2, temptLitem)
        self.__tableWidget.setItem(row, 3, temptZitem)

        self.__tableWidget.item(row, 0).setFlags(Qt.ItemIsEditable)
        self.__tableWidget.item(row, 1).setFlags(Qt.ItemIsEditable)

        return temptLitem

    def reload(self):

        # initial table
        try:
            self.__tableWidget.setRowCount(0)
            self.__tableWidget.disconnect()
        except:
            pass

        # create SBK line format
        sbkTemptList = []  # [[l1,z1],[l2,z2]...[ln,zn]]

        # add other point
        self.__tableData.sort(key=lambda s: s[2])
        for point in self.__tableData:
            self.__addLine(point[0], point[1], point[2], point[3])
            sbkTemptList.append([point[2], point[3]])

        # add onChange signal
        self.__tableWidget.cellChanged.connect(self.__reloadRow)

        # replot SBK line
        self.__plotClass.rePlotSBK(sbkTemptList)

    def __reloadRow(self, row: int, column: int):
        if column >= 2 and column <= 3:
            temptL = None
            try:
                temptL = float(self.__tableWidget.item(row, column).text())
                self.__tableData[row][column] = temptL
            except:
                temptL = self.__tableData[row][column]

            temptXY = self.__lengthToXY(temptL)
            self.__tableData[row][0] = temptXY[0]
            self.__tableData[row][1] = temptXY[1]

            self.__tableData.sort(key=lambda s: s[2])
            self.reload()

    def __lengthToXY(self, l: float) -> list:

        # normalize y-z chart, which center y=0
        deltX = self.__endX - self.__startX
        deltY = self.__endY - self.__startY

        temptX = self.__startX + deltX * \
            ((l + self.__totalLength/2) / self.__totalLength)
        temptY = self.__startY + deltY * \
            ((l + self.__totalLength/2) / self.__totalLength)
        return [temptX, temptY]

    def clear(self):
        self.__tableData.clear()
        self.__tableWidget.disconnect()
        self.__tableWidget.setRowCount(0)
# ===================================TEST===================

    def __test__itemOnChanged(self, row: int, column: int):
        print("item on change " + str(row) + "\t" + str(column))

    def __test__itemOnEnter(self):
        print("item on enter")
