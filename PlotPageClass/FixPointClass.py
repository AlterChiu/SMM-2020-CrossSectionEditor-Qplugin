from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtGui import QDoubleValidator
import pyqtgraph as pyqtgraph

import traceback

from .PlotWidgetClass import PlotWidgetClass


class FixPointClass:

    def __init__(self, dlg, plotWidget: PlotWidgetClass):

        # constant
        self.__dlg = dlg
        self.__plotWidget = plotWidget
        self.__validator = QDoubleValidator()

        # text edit
        self.__leftFixPointYWidget = self.__dlg.findChild(
            QLineEdit, "leftFixPointY")
        self.__leftFixPointYWidget.setValidator(self.__validator)
        self.__leftFixPointYWidget.textChanged.connect(lambda: self.plot())

        self.__leftFixPointZWidget = self.__dlg.findChild(
            QLineEdit, "leftFixPointZ")
        self.__leftFixPointZWidget.setValidator(self.__validator)
        self.__leftFixPointZWidget.textChanged.connect(lambda: self.plot())

        self.__rightFixPointYWidget = self.__dlg.findChild(
            QLineEdit, "rightFixPointY")
        self.__rightFixPointYWidget.setValidator(self.__validator)
        self.__rightFixPointYWidget.textChanged.connect(lambda: self.plot())

        self.__rightFixPointZWidget = self.__dlg.findChild(
            QLineEdit, "rightFixPointZ")
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

    def plot(self):
        self.__plotWidget.clearFixPoint()
        try:
            temptLeftY = float(self.__leftFixPointYWidget.text())
            temptLeftZ = float(self.__leftFixPointZWidget.text())
            self.__plotWidget.setLeftFixPoint(temptLeftY, temptLeftZ)

        except:
            traceback.print_exc()
            self.__plotWidget.setLeftFixPoint(
                self.__leftFixPoint["y"], self.__leftFixPoint["z"])

        try:
            temptRightY = float(self.__rightFixPointYWidget.text())
            temptRightZ = float(self.__rightFixPointZWidget.text())
            self.__plotWidget.setRightFixPoint(temptRightY, temptRightZ)
        except:
            traceback.print_exc()
            self.__plotWidget.setRightFixPoint(
                 self.__rightFixPoint["y"], self.__rightFixPoint["z"])

        self.__plotWidget.plotFixPoints()

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
