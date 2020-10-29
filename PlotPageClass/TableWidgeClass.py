from PyQt5.QtWidgets import QTableWidget,QFrame,QAbstractItemView,QHeaderView,QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import statistics
import traceback
import sys
import math

class TableWidgeClass:

   

    def __init__(self , tableWidget:QTableWidget):


        # set table
        #----------------------------
        self.__tableWidget = tableWidget
        self.__tableData = [] #[[x,y,l,z] , [x,y,l,z].....]
        
        #self.__tableWidget.horizontalHeader().setSectionResizeMode(5,QHeaderView.Stretch)# set 6 column autoSize
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
        self.__tableData = []
        self.__startX = x
        self.__startY = y
        self.__startZ = z

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
        self.__tableData = []
        self.__endX = x
        self.__endY = y
        self.__endZ = z

        try:
            deltX = self.__startX - self.__endX
            deltY = self.__startY - self.__endY
            self.__totalLength = math.sqrt(math.pow(deltX,2) + math.pow(deltY,2))
        except:
            pass

    def addPoint(self , l:float , z:float):
        try:
            if abs(l) <= self.__totalLength/2.0:

                # normalize y-z chart, which center y=0
                temptXY = self.__lengthToXY(l)
                temptX = temptXY[0]
                temptY = temptXY[1]

                # add to collection
                self.__tableData.append([temptX , temptY , l , z])
                self.__tableData.sort(key = lambda s:s[2])

                # reload
                self.__reload()

            else:
                print("invalid point")
        except Exception:
            traceback.print_exc(file=sys.stdout)
            print("missing points:")
            print("startPoint: " + str(self.__startX)  + "\t" + str(self.__startY))
            print("endPoint: " + str(self.__endX) + "\t" + str(self.__endY))
        
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
        for row in range(0,len(self.__tableData)):
            if self.__tableData[row][3]*range > 0:
                temptL = self.__tableData[row][2] + moveL

                # change value then reload selected row    
                if math.abs(temptL) < self.__totalLength/2 and temptL*range>0:
                    temptXY = self.__lengthToXY(temptL)
                    self.setValue(row,0 , temptXY[0])
                    self.setValue(row,1 , temptXY[1])
                    self.__reloadRow(row)

    def __tableDataMoveZ(self , moveZ:float , range:int):# range <0:left , >0:right
        
        # detect by range
        for row in range(0,len(self.__tableData)):
            if self.__tableData[row][3]*range > 0:
                temptZ = self.__tableData[row][3] + moveZ
                self.setValue(row,3,temptZ)


    # private function
    #----------------------------------------------------------
    def __addLine(self , x:float , y:float , l:float , z:float):
        row = self.__tableWidget.rowCount()
        self.__tableWidget.insertRow(row)

        self.__tableWidget.setItem(row , 0 , QTableWidgetItem(str(x)))
        self.__tableWidget.setItem(row , 1 , QTableWidgetItem(str(y)))
        self.__tableWidget.setItem(row , 2 , QTableWidgetItem(str(l)))
        self.__tableWidget.setItem(row , 3 , QTableWidgetItem(str(z)))

        self.__tableWidget.item(row,0).setFlags(Qt.ItemIsEditable)
        self.__tableWidget.item(row,1).setFlags(Qt.ItemIsEditable)

    def __reload(self):
        self.__tableWidget.setRowCount(0)

        # add startPoint
        #self.__addLine(self.__startX , self.__startY , 0 , self.__startZ)

        # add endPoint
        #self.__addLine(self.__endX , self.__endY , self.__totalLength , self.__endZ)

        # add other point
        for index in range(-1 , len(self.__tableData)*-1-1 , -1):
            point = self.__tableData[index]
            self.__addLine(point[0] , point[1] , point[2] , point[3])


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









