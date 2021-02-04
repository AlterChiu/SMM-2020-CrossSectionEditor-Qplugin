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
        self.__tableData = []
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
        self.__tableData = []
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

    # valuelist = [x,y,z]

    def replace(self, valueList: list):
        # clear table data
        self.__tableData = []

        # set start end points
        self.setStartPoint(valueList[0][0], valueList[0][1], valueList[0][2])
        self.setEndPoint(valueList[-1][0], valueList[-1][1], valueList[-1][2])

        # set other point to y-z
        temptLList = []
        temptZList = []
        for index in range(0, len(valueList)):
            deltX = valueList[index][0] - self.__startX
            deltY = valueList[index][1] - self.__startY
            temptLength = math.sqrt(math.pow(deltX, 2)+math.pow(deltY, 2))

            temptLList.append(temptLength)
            temptZList.append(valueList[index][2])

        # add point
        midL = (max(temptLList) + min(temptLList))/2
        for index in range(0, len(temptLList)):
            self.addPoint(temptLList[index]-midL, temptZList[index])

        self.reload()

    def rightDataMove(self, ratio: float = 1.0,  moveL: float = 0):
        self.__tableDataRatioMoveL(ratio=ratio, moveL=moveL, direction=1)
        self.reload()

    def leftDataMove(self,  ratio: float = 1.0, moveL: float = 0):
        self.__tableDataRatioMoveL(ratio=ratio, moveL=moveL, direction=-1)
        self.reload()

    def topDataMove(self, ratio: float = 1.0, moveZ: float = 0):
        self.__tableDataRatioMoveZ(ratio=ratio, moveZ=moveZ, direction=1)
        self.reload()

    def bottomDataMove(self, ratio: float = 1.0, moveZ: float = 0):
        self.__tableDataRatioMoveZ(ratio=ratio, moveZ=moveZ, direction=-1)
        self.reload()

    def dataMove(self, moveZ: float = 0, moveL: float = 0):
        for row in range(0, len(self.__tableData)):
            temptL = self.__tableData[row][2] + moveL
            temptXY = self.__lengthToXY(temptL)

            self.__tableData[row][0] = temptXY[0]
            self.__tableData[row][1] = temptXY[1]
            self.__tableData[row][2] = temptL
            self.__tableData[row][3] = self.__tableData[row][3] + moveZ
        self.reload()

    def dataZoom(self, zoom: float = 0):
        if zoom > 0:
            self.__tableDataRatioMoveL(zoom, 0)
            self.__tableDataRatioMoveZ(zoom, 0)
        self.reload()

    # move => persantage to move
    # moveL = 1.05, which L will change from 1 to 1.05 (2 to 2.10), same as moveZ
    # direction <0:left , >0:right , 0: bothSide
    def __tableDataRatioMoveL(self, ratio: float = 1.0, moveL: float = 0, direction: int = 0):

        # get middle L
        temptLList = []
        for point in self.__tableData:
            temptLList.append(point[2])
        middleL = (max(temptLList) + min(temptLList))/2

        # moving
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

        # ratio
        if ratio != 1.0 and direction != 0:

            # get limit L
            rightLimit = None
            leftLimit = None
            napPoint = None
            if direction > 0:
                rightLimit = max(temptLList)
                leftLimit = middleL
                napPoint = rightLimit

            else:
                rightLimit = middleL
                leftLimit = min(temptLList)
                napPoint = leftLimit

            # get close to limit value
            for row in range(0, len(self.__tableData)):
                temptL = self.__tableData[row][2]
                if (self.__tableData[row][2] - middleL)*direction > 0:
                    temptL = temptL + \
                        abs(napPoint - temptL) * ratio * direction

                    # check value range
                    if temptL < leftLimit:
                        temptL = leftLimit
                    elif temptL > rightLimit:
                        temptL = rightLimit

                temptXY = self.__lengthToXY(temptL)
                self.__tableData[row][0] = temptXY[0]
                self.__tableData[row][1] = temptXY[1]
                self.__tableData[row][2] = temptL

    # direction <0:bottom , >0:top, 0: bothSide
    def __tableDataRatioMoveZ(self, ratio: float = 1.0, moveZ: float = 0.0, direction: int = 0):

        # get middle Z
        temptZList = []
        for point in self.__tableData:
            temptZList.append(point[3])
        middleZ = (max(temptZList) + min(temptZList))/2

        # moving
        for row in range(0, len(self.__tableData)):
            temptZ = self.__tableData[row][3]

            if direction == 0:
                temptZ = self.__tableData[row][3] + moveZ

            elif (self.__tableData[row][3] - middleZ)*direction > 0:
                temptZ = self.__tableData[row][3] + moveZ

            self.__tableData[row][3] = temptZ

        # ratio
        if ratio != 1.0 and direction != 0:

            # get limit Z
            topLimit = None
            bottomLimit = None
            napPoint = None
            if direction > 0:
                topLimit = max(temptZList)
                bottomLimit = middleZ
                napPoint = topLimit

            else:
                topLimit = middleZ
                bottomLimit = min(temptZList)
                napPoint = bottomLimit

            # get close to limit value
            for row in range(0, len(self.__tableData)):
                temptZ = self.__tableData[row][3]
                if (self.__tableData[row][3] - middleZ)*direction > 0:
                    temptZ = temptZ + \
                        abs(napPoint - temptZ) * ratio * direction

                    # check value range
                    if temptZ < bottomLimit:
                        temptZ = bottomLimit
                    elif temptZ > topLimit:
                        temptZ = topLimit

                self.__tableData[row][3] = temptZ

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
        self.__tableData = []
        self.__tableWidget.disconnect()
        self.__tableWidget.setRowCount(0)
# ===================================TEST===================

    def __test__itemOnChanged(self, row: int, column: int):
        print("item on change " + str(row) + "\t" + str(column))

    def __test__itemOnEnter(self):
        print("item on enter")
