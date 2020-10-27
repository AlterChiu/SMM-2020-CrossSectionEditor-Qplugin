from PyQt5.QtWidgets import QTableWidget,QFrame,QAbstractItemView,QHeaderView,QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import math
import statistics

class TableWidgeClass:

    __tableData = None #[[x,y,l,z] , [x,y,l,z].....]

    def __init__(self , tableWidget:QTableWidget):

        # setFont
        #----------------------------
        self.__titleFont = QFont('Microsoft YaHei', 14)
        self.__titleFont.setBold(True)
        self.__itemFont = QFont('Microsoft YaHei',12)

        # set table
        #----------------------------
        self.__tableWidget = tableWidget
        
        # setTitle
        self.__tableWidget.horizontalHeader().setFont(self.__titleFont) #font
        self.__tableWidget.horizontalHeader().setFixedHeight(50) #title height
        self.__tableWidget.setColumnCount(6) # set 6 column
        #self.__tableWidget.horizontalHeader().setSectionResizeMode(5,QHeaderView.Stretch)# set 6 column autoSize
        self.__tableWidget.setHorizontalHeaderLabels(['X','Y','L','Z'])# set title text
        self.__tableWidget.horizontalHeader().setSectionsClickable(False) # unable click title

        # data
        #----------------------------
        self.__startX = None
        self.__startY = None
        self.__startZ = None
        self.__endX = None
        self.__endY = None
        self.__endZ = None

        self.__totalLength = None

    # public finctions
    #--------------------------------------------------------------
    def setStartPoint(self , x:float , y:float , z:float):
        self.__startX = None
        self.__startY = None
        self.__startZ = None
        __tableData = []
        self.__startX = x
        self.__startY = y

        try:
            deltX = self.__startX - self.__endX
            deltY = self.__startY - self.__endY
            self.__totalLength = math.sqrt(math.pow(deltX,2) + math.pow(deltY,2))
        except:
            pass

    def setEndPoint(self , x:float , y:float , z:float):
        self.__endX = None
        self.__endY = None
        self.__endZ = None
        __tableData = []
        self.__endX = x
        self.__endY = y

        try:
            deltX = self.__startX - self.__endX
            deltY = self.__startY - self.__endY
            self.__totalLength = math.sqrt(math.pow(deltX,2) + math.pow(deltY,2))
        except:
            pass

    def addPoint(self , l:float , z:float):
        try:


            if math.abs(l) <= self.__totalLength/2:

                # normalize y-z chart, which center y=0
                temptXY = self.__lengthToXY(l)
                temptX = temptXY[0]
                temptY = temptXY[1]

                # add to collection
                self.__tableData.append([temptX , temptY , l , z])
                self.__tableData.sort(key = lambda s:s[2])

                # add to table
                self.__addLine(temptX , temptY , l ,z)

                # sorted
                self.__tableWidget.sortByColumn(2)
            else:
                print("invalid point")
        except:
            print("missing startEnd points: \r\n")
            print("startPoint: " + self.__startX  + "\t" + self.__startY + "\r\n")
            print("endPoint: " + self.__endX + "\t" + self.__endY + "\r\n")
        
    def deletPoint(self , index:int):
        try:
            self.__tableData.pop(index)
        except:
            pass
    
    # only operate after l,z edit
    def setValue(self , row:int , column:int , value:float)->list: #return [x,y]
        try:
            self.__tableWidget.setItem(row , column , QTableWidgetItem(value))
            self.__reloadRow(row)
        except:
            print("table setValue caught error")
            pass











    # advace functions
    #----------------------------------------------------------

    # valuelist = [x,y,z]
    def replace(self , valueList:list):

        # sorted by x
        sortedList = sorted(valueList , key= lambda s:s[0])

        # set start end points
        self.setStartPoint(sortedList[0][0] , sortedList[0][1])
        self.setEndPoint(sortedList[-1][0] , sortedList[-1][1])

        # set other point to y-z
        temptLList=[]
        temptZList=[]
        for index in range(1,len(valueList)-1):
            deltX = valueList[index][0] - self.__startX
            deltY = valueList[index][1] - self.__startY
            temptLength = math.sqrt(math.pow(deltX,2)+math.pow(deltY,2))
            
            temptLList.append(temptLength)
            temptLList.append(valueList[index][2])

        #add point
        meanL = statistics.mean(temptLList)
        for index in range(0,len(temptLList)):
            self.addPoint(meanL - temptLList[index] , temptZList[index])

    def rightDataMove(self , moveL:float=0 , moveZ:float=0):
        if moveL != 0:
            self.__tableDataMoveL(moveL,1)
        
        if moveZ !=0:
            self.__tableDataMoveZ(moveZ,1)
    
    def leftDataMove(self , moveL:float=0 , moveZ:float=0):
        if moveL != 0:
            self.__tableDataMoveL(moveL,-1)
        
        if moveZ !=0:
            self.__tableDataMoveZ(moveZ,-1)

    def __tableDataMoveL(self , moveL:float , range:int): # range <0:left , >0:right

        # detect by range
        for row in range(0,len(__tableData)):
            if __tableData[row][3]*range > 0:
                temptL = __tableData[row][2] + moveL

                # change value then reload selected row    
                if math.abs(temptL) < self.__totalLength/2 and temptL*range>0:
                    temptXY = self.__lengthToXY(temptL)
                    self.setValue(row,0 , temptXY[0])
                    self.setValue(row,1 , temptXY[1])
                    self.__reloadRow(row)

    def __tableDataMoveZ(self , moveZ:float , range:int):# range <0:left , >0:right
        
        # detect by range
        for row in range(0,len(__tableData)):
            if __tableData[row][3]*range > 0:
                temptZ = self.__tableData[row][3] + moveZ
                self.setValue(row,3,temptZ)


    # private function
    #----------------------------------------------------------
    def __addLine(self , x:float , y:float , l:float , z:float):
        row = self.__tableWidget.rowCount()
        self.__tableWidget.setRowCount(row+1)

        self.__tableWidget.setItem(row , 0 , QTableWidgetItem(x))
        self.__tableWidget.setItem(row , 1 , QTableWidgetItem(y))
        self.__tableWidget.setItem(row , 2 , QTableWidgetItem(l))
        self.__tableWidget.setItem(row , 3 , QTableWidgetItem(z))

        self.__tableWidget.item(row,0).setFlags(Qt.ItemIsEditable)
        self.__tableWidget.item(row,1).setFlags(Qt.ItemIsEditable)

    def __reload(self , tableData:list=__tableData):
        self.__tableWidget.clearContents()

        # add startPoint
        #self.__addLine(self.__startX , self.__startY , 0 , self.__startZ)

        # add endPoint
        #self.__addLine(self.__endX , self.__endY , self.__totalLength , self.__endZ)

        # add other point
        for point in tableData:
             self.__addLine(point[0] , point[1] , point[2] , point[3])

        # sorted
        self.__tableWidget.sortByColumn(2)

    def __reloadRow(self,row:int):
        temptL = self.__tableData[row][2]
        temptXY = self.__lengthToXY(temptL)
        self.__tableWidget.setItem(row , 0 , QTableWidgetItem(temptXY[0]))
        self.__tableWidget.setItem(row , 1 , QTableWidgetItem(temptXY[1]))

    def __lengthToXY(self,l:float)->list:
        
        # normalize y-z chart, which center y=0
        deltX = self.__endX - self.__startX
        deltY = self.__endY - self.__startY

        temptX = self.__startX + deltX * (1 + l/self.__totalLength)
        temptY = self.__startY + deltY * (1 + l/self.__totalLength)
        return [temptX , temptY]









