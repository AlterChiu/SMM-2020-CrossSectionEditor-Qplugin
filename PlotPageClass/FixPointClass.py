from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtGui import QDoubleValidator
import pyqtgraph as pyqtgraph

import sys
import traceback

from .PlotWidget.PlotWidgetClass import PlotWidgetClass
from .TableWidget.TableWidgeClass import TableWidgeClass


class FixPointClass:

    # dataList format = [[x,y,l,z]....]
    def __init__(self, dlg, prefixName: str, plotWidget: PlotWidgetClass, dataList: list):

        # constant
        self.__dlg = dlg
        self.__plotWidget = plotWidget
        self.__validator = QDoubleValidator()
        self.__prefixName = prefixName
        self.__tableWidgeClass = TableWidgeClass
        self.__dataList = dataList

        # text edit
        self.__leftFixPointYWidget = self.__dlg.findChild(
            QLineEdit, prefixName + "leftFixPointY")
        self.__leftFixPointYWidget.setValidator(self.__validator)
        self.__leftFixPointYWidget.textChanged.connect(lambda: self.plot())

        self.__leftFixPointZWidget = self.__dlg.findChild(
            QLineEdit, prefixName+"leftFixPointZ")
        self.__leftFixPointZWidget.setValidator(self.__validator)
        self.__leftFixPointZWidget.textChanged.connect(lambda: self.plot())

        self.__rightFixPointYWidget = self.__dlg.findChild(
            QLineEdit, prefixName+"rightFixPointY")
        self.__rightFixPointYWidget.setValidator(self.__validator)
        self.__rightFixPointYWidget.textChanged.connect(lambda: self.plot())

        self.__rightFixPointZWidget = self.__dlg.findChild(
            QLineEdit, prefixName+"rightFixPointZ")
        self.__rightFixPointZWidget.setValidator(self.__validator)
        self.__rightFixPointZWidget.textChanged.connect(lambda: self.plot())

        self.__leftFixPoint = {"y": 0.0, "z": 0.0}
        self.__rightFixPoint = {"y": 0.0, "z": 0.0}

    def setLeftFixPointYZ(self, y: float, z: float):
        try:
            self.__leftFixPointYWidget.setText(str(y))
            self.__leftFixPoint["y"] = y

            self.__leftFixPointZWidget.setText(str(z))
            self.__leftFixPoint["z"] = z
        except:
            traceback.print_exc()
            print("lefttFixPoint convert exception")

    def setRightFixPointYZ(self, y: float, z: float):
        try:
            self.__rightFixPointYWidget.setText(str(y))
            self.__rightFixPoint["y"] = y

            self.__rightFixPointZWidget.setText(str(z))
            self.__rightFixPoint["z"] = z
        except:
            traceback.print_exc()
            print("rightFixPoint convert exception")

    def __autoDetectRightZ(self):
        temptL = float(self.__rightFixPointYWidget.text())
        temptZ = self.__autoDetectZ(temptL)

        if(temptZ != None):
            self.__rightFixPointZWidget.setText(str(temptZ))
        self.plot()

    def __autoDetectLeftZ(self):
        temptL = float(self.__leftFixPointYWidget.text())
        temptZ = self.__autoDetectZ(temptL)
        
        if(temptZ != None):
            self.__leftFixPointZWidget.setText(str(temptZ))
        self.plot()
    
    def __autoDetectZ(self , l:float):
        
        smallerValues = [] #[[y,z]]
        biggerValues = [] #[[y,z]]
        
        for value in self.__dataList:
            temptL = value[2]
            
            if temptL > l:
                biggerValues.append([temptL , value[3]])
            else:
                smallerValues.append([temptL , value[3]])
                
        smallerValue = None
        try:
            max(smallerValue , key= lambda x: x[2])
        except:
            pass
        
        biggerValue = None
        try:
            min(biggerValue , key=lambda x:x[2])
        except:
            pass
        
        if biggerValue == None and smallerValue == None:
            return None
        elif biggerValue == None:
            return smallerValue[3]
        elif smallerValue == None:
            return biggerValue[3]
        else:
            totalL = biggerValue[2] - smallerValue[2]
            dsiL = l - smallerValue[2]
            totalZ = biggerValue[3] - smallerValue[3] 
            return smallerValue[3] + totalZ*(disL/totalL)
                    
    def plot(self):
        self.__plotWidget.clearFixPoint()
        try:
            temptLeftY = float(self.__leftFixPointYWidget.text())
            temptLeftZ = float(self.__leftFixPointZWidget.text())
            self.__plotWidget.setFixPoint(
                temptLeftY, temptLeftZ, self.__prefixName, "left")

        except:
            traceback.print_exc()
            self.__plotWidget.setFixPoint(
                self.__leftFixPoint["y"], self.__leftFixPoint["z"], self.__prefixName, "left")

        try:
            temptRightY = float(self.__rightFixPointYWidget.text())
            temptRightZ = float(self.__rightFixPointZWidget.text())
            self.__plotWidget.setFixPoint(
                temptRightY, temptRightZ, self.__prefixName, "right")
        except:
            traceback.print_exc()
            self.__plotWidget.setFixPoint(
                self.__rightFixPoint["y"], self.__rightFixPoint["z"], self.__prefixName, "right")

        self.__plotWidget.plotFixPoints(self.__prefixName)

    def getRightFixPoint(self) -> list:  # [y,z]
        return [self.__rightFixPointYWidget.text(), self.__rightFixPointZWidget.text()]

    def getLeftFixPoint(self) -> list:  # [y,z]
        return [self.__leftFixPointYWidget.text(), self.__leftFixPointZWidget.text()]

    def clear(self):
        self.__rightFixPointYWidget.setText("")
        self.__rightFixPointZWidget.setText("")
        self.__leftFixPointYWidget.setText("")
        self.__leftFixPointZWidget.setText("")

    def blockTextEdit(self):
        self.__leftFixPointYWidget.setEnabled(False)
        self.__leftFixPointZWidget.setEnabled(False)
        self.__rightFixPointYWidget.setEnabled(False)
        self.__rightFixPointZWidget.setEnabled(False)

    def unBlockTextEdit(self):
        self.__leftFixPointYWidget.setEnabled(True)
        self.__leftFixPointZWidget.setEnabled(True)
        self.__rightFixPointYWidget.setEnabled(True)
        self.__rightFixPointZWidget.setEnabled(True)
