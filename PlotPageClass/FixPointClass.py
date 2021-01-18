from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication,QLineEdit
from PyQt5.QtGui import QDoubleValidator
import pyqtgraph as pyqtgraph

import traceback

from .PlotWidgetClass import PlotWidgetClass

class FixPointClass:

    def __init__(self , dlg, plotPage:PlotWidgetClass):
        
        # constant
        self.__dlg = dlg
        self.__plotpage = plotPage
        self.__validator = QDoubleValidator()

        # text edit
        self.__leftFixPointY = self.__dlg.findChild(QLineEdit , "leftFixPointY")
        self.__leftFixPointY.setValidator(self.__validator)
        self.__leftFixPointY.returnPressed.connect(lambda:self.plot())
        
        self.__leftFixPointZ = self.__dlg.findChild(QLineEdit , "leftFixPointZ")
        self.__leftFixPointZ.setValidator(self.__validator)
        self.__leftFixPointZ.returnPressed.connect(lambda:self.plot())

        self.__rightFixPointY = self.__dlg.findChild(QLineEdit , "rightFixPointY")
        self.__rightFixPointY.setValidator(self.__validator)
        self.__rightFixPointY.returnPressed.connect(lambda:self.plot())

        self.__rightFixPointZ = self.__dlg.findChild(QLineEdit , "rightFixPointZ")
        self.__rightFixPointZ.setValidator(self.__validator)
        self.__rightFixPointZ.returnPressed.connect(lambda:self.plot())



    def setLeftFixPointYZ(self , y:float , z:float):
        try:
            self.__leftFixPointY.setText(str(y))
            self.__leftFixPointZ.setText(str(z))
        except:
            traceback.print_exc()
            print("lefttFixPoint convert exception")
    
    def setRightFixPointYZ(self , y:float , z:float):
        try:
            self.__rightFixPointY.setText(str(y))
            self.__rightFixPointZ.setText(str(z))
        except:
            traceback.print_exc()
            print("rightFixPoint convert exception")

    def plot(self):
        self.__plotpage.clearFixPoint()
        try:
            temptLeftY = float(self.__leftFixPointY.text())
            temptLeftZ = float(self.__leftFixPointZ.text())
            self.__plotpage.setLeftFixPoint(temptLeftY,temptLeftZ)

            temptRightY = float(self.__rightFixPointY.text())
            temptRightZ = float(self.__rightFixPointZ.text())
            self.__plotpage.setRightFixPoint(temptRightY,temptRightZ)
            
            self.__plotpage.plotFixPoints()
        except:
            traceback.print_exc()
            print("error while plot fixPoints")

    def getRightFixPoint(self)->list: # [y,z]
        return [self.__rightFixPointY.text() , self.__rightFixPointZ.text()]

    def getLeftFixPoint(self)->list: # [y,z]
        return [self.__leftFixPointY.text() , self.__leftFixPointZ.text()]

    def clear(self):
        self.__rightFixPointY.setText("")
        self.__rightFixPointZ.setText("")
        self.__leftFixPointY.setText("")
        self.__leftFixPointZ.setText("")
        

    def blockTextEdit(self):
        self.__leftFixPointY.setEnabled(False)
        self.__leftFixPointZ.setEnabled(False)
        self.__rightFixPointY.setEnabled(False)
        self.__rightFixPointZ.setEnabled(False)



    def unBlockTextEdit(self):
        self.__leftFixPointY.setEnabled(True)
        self.__leftFixPointZ.setEnabled(True)
        self.__rightFixPointY.setEnabled(True)
        self.__rightFixPointZ.setEnabled(True)
