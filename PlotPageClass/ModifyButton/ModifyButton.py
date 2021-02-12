from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QComboBox

import traceback

from ..TableWidget.TableWidgeClass import TableWidgeClass


class ModifyButtonClass:

    def __init__(self, dlg, tableClass: TableWidgeClass):
        self.__dlg = dlg
        self.__tableClass = tableClass
        
        self.__moveUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveUp")
        self.__moveUpButton.clicked.connect(lambda: self.__moveUp())

        self.__moveDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveDown")
        self.__moveDownButton.clicked.connect(lambda: self.__moveDown())

        self.__moveRightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveRight")
        self.__moveRightButton.clicked.connect(lambda: self.__moveRight())

        self.__moveLeftButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveLeft")
        self.__moveLeftButton.clicked.connect(lambda: self.__moveLeft())

        self.__moveTLUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveTLUp")
        self.__moveTLUpButton.clicked.connect(lambda: self.__moveTLUp())

        self.__moveTLDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveTLDown")
        self.__moveTLDownButton.clicked.connect(lambda: self.__moveTLDown())

        self.__moveTRUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveTRUp")
        self.__moveTRUpButton.clicked.connect(lambda: self.__moveTRUp())

        self.__moveTRDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveTRDown")
        self.__moveTRDownButton.clicked.connect(lambda: self.__moveTRDown())

        self.__moveBLUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBLUp")
        self.__moveBLUpButton.clicked.connect(lambda: self.__moveBLUp())

        self.__moveBLDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBLDown")
        self.__moveBLDownButton.clicked.connect(lambda: self.__moveBLDown())

        self.__moveBLLeftButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBLLeft")
        self.__moveBLLeftButton.clicked.connect(lambda: self.__moveBLLeft())

        self.__moveBLRightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBLRight")
        self.__moveBLRightButton.clicked.connect(lambda: self.__moveBLRight())

        self.__moveBRUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBRUp")
        self.__moveBRUpButton.clicked.connect(lambda: self.__moveBRUp())

        self.__moveBRDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBRDown")
        self.__moveBRDownButton.clicked.connect(lambda: self.__moveBRDown())

        self.__moveBRLeftButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBRLeft")
        self.__moveBRLeftButton.clicked.connect(lambda: self.__moveBRLeft())

        self.__moveBRRightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBRRight")
        self.__moveBRRightButton.clicked.connect(lambda: self.__moveBRRight())

        self.__ratioTLUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioTLUp")
        self.__ratioTLUpButton.clicked.connect(lambda: self.__ratioTLUp())

        self.__ratioTLDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioTLDown")
        self.__ratioTLDownButton.clicked.connect(lambda: self.__ratioTLDown())

        self.__ratioTRUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioTRUp")
        self.__ratioTRUpButton.clicked.connect(lambda: self.__ratioTRUp())

        self.__ratioTRDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioTRDown")
        self.__ratioTRDownButton.clicked.connect(lambda: self.__ratioTRDown())

        self.__ratioBLUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBLUp")
        self.__ratioBLUpButton.clicked.connect(lambda: self.__ratioBLUp())

        self.__ratioBLDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBLDown")
        self.__ratioBLDownButton.clicked.connect(lambda: self.__ratioBLDown())

        self.__ratioBLLeftButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBLLeft")
        self.__ratioBLLeftButton.clicked.connect(lambda: self.__ratioBLLeft())

        self.__ratioBLRightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBLRight")
        self.__ratioBLRightButton.clicked.connect(
            lambda: self.__ratioBLRight())

        self.__ratioBRUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBRUp")
        self.__ratioBRUpButton.clicked.connect(lambda: self.__ratioBRUp())

        self.__ratioBRDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBRDown")
        self.__ratioBRDownButton.clicked.connect(lambda: self.__ratioBRDown())

        self.__ratioBRLeftButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBRLeft")
        self.__ratioBRLeftButton.clicked.connect(lambda: self.__ratioBRLeft())

        self.__ratioBRRightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBRRight")
        self.__ratioBRRightButton.clicked.connect(
            lambda: self.__ratioBRRight())

    def __moveUp(self):
        self.__tableClass.dataMove(moveZ=0.1)

    def __moveDown(self):
        self.__tableClass.dataMove(moveZ=-0.1)

    def __moveRight(self):
        self.__tableClass.dataMove(moveL=1.0)

    def __moveLeft(self):
        self.__tableClass.dataMove(moveL=-1.0)
        
    def __moveTLUp(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=-1.0, ratioZ=0.0, moveZ=0.1, directionZ=1.0)

    def __moveTLDown(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=-1.0, ratioZ=0.0, moveZ=-0.1, directionZ=1.0)

    def __moveTRUp(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=1, ratioZ=0.0, moveZ=0.1, directionZ=1.0)

    def __moveTRDown(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=1, ratioZ=0.0, moveZ=-0.1, directionZ=1.0)

    def __moveBLUp(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=-1.0, ratioZ=0.0, moveZ=0.1, directionZ=-1.0)

    def __moveBLDown(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=-1.0, ratioZ=0.0, moveZ=-0.1, directionZ=-1.0)

    def __moveBLLeft(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=-0.1, directionL=-1.0, ratioZ=0.0, moveZ=0.0, directionZ=0)

    def __moveBLRight(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.1, directionL=-1.0, ratioZ=0.0, moveZ=0.0, directionZ=0)

    def __moveBRUp(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=1, ratioZ=0.0, moveZ=0.1, directionZ=-1.0)

    def __moveBRDown(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=1, ratioZ=0.0, moveZ=-0.1, directionZ=-1.0)

    def __moveBRLeft(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=-0.1, directionL=1, ratioZ=0.0, moveZ=0.0, directionZ=0)

    def __moveBRRight(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.1, directionL=1, ratioZ=0.0, moveZ=0.0, directionZ=0)

    def __ratioTLUp(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=-1.0, ratioZ=0.15, moveZ=0.0, directionZ=1.0)

    def __ratioTLDown(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=-1.0, ratioZ=-0.15, moveZ=0.0, directionZ=1.0)

    def __ratioTRUp(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=1, ratioZ=0.15, moveZ=0.0, directionZ=1.0)

    def __ratioTRDown(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=1, ratioZ=-0.15, moveZ=0.0, directionZ=1.0)

    def __ratioBLUp(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=-1.0, ratioZ=-0.15, moveZ=0.0, directionZ=-1.0)

    def __ratioBLDown(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=-1.0, ratioZ=0.15, moveZ=0.0, directionZ=-1.0)

    def __ratioBLLeft(self):
        self.__tableClass.dataMove(
            ratioL=0.15, moveL=0.0, directionL=-1.0, ratioZ=0.0, moveZ=0.0, directionZ=0)

    def __ratioBLRight(self):
        self.__tableClass.dataMove(
            ratioL=-0.15, moveL=0.0, directionL=-1.0, ratioZ=0.0, moveZ=0.0, directionZ=0)

    def __ratioBRUp(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=1, ratioZ=-0.15, moveZ=0.0, directionZ=-1.0)

    def __ratioBRDown(self):
        self.__tableClass.dataMove(
            ratioL=0.0, moveL=0.0, directionL=1, ratioZ=0.15, moveZ=0.0, directionZ=-1.0)

    def __ratioBRLeft(self):
        self.__tableClass.dataMove(
            ratioL=-0.15, moveL=0.0, directionL=1, ratioZ=0.0, moveZ=0.0, directionZ=0)

    def __ratioBRRight(self):
        self.__tableClass.dataMove(
            ratioL=0.15, moveL=0.0, directionL=1, ratioZ=0.0, moveZ=0.0, directionZ=0)
