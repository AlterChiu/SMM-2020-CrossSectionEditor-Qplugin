from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QComboBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsWkbTypes, QgsProcessingUtils, QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem

from ..FramePage import BankLinePage
from .PlotWidget import PlotWidgetClass
import requests
import traceback
import json

import sys


class BankLineClass:
    def __init__(self, selectedLayer, streamId):

        # initial page
        self.__dlg = BankLinePage()
        self.__dlg.show()
        self.__layer = selectedLayer

        # plotPoage
        self.__currentSelection = {
            "activeIndex": 0,
            "hoverIndex": None,
            "maximumIndex": None
        }

        # initial comboBox
        self.__streamComboBox = self.__dlg.findChild(
            QtWidgets.QComboBox, "streamSelection")
        self.__initialStreamComboBox()

        # initial button
        self.__leftButton = self.__dlg.findChild(QtWidgets.QPushButton, "left")
        self.__leftButton.clicked.connect(lambda: self.__selectionGoLeft())

        self.__rightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "right")
        self.__rightButton.clicked.connect(lambda: self.__selectionGoRight())

        self.__selectButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "select")
        self.__selectButton.clicked.connect(lambda: self.__select())
        
        # datas
        # {
        #     # "collected by referntId"
        #     referentId :

        #     # sorted by distance
        #     [
        #         {
        #             id: id,
        #             leftHight : "the highest level of the left crossSection",
        #             rightHight : "the highest level of the right crossSection",
        #             bottom : "the lowest level of the crossSection",
        #             distance : "distance from begining"
        #         }
        #     ]
        # }
        self.__data = {}
        self.initialStreamData()
        self.__initialStreamComboBox()
        
        # initial plotWidget
        self.__plotWidget = self.__dlg.findChild(
            pyqtgraph.PlotWidget, "plotWidget")
        self.__plotClass = PlotWidgetClass(self.__plotWidget , self.__data)
        

    def __initialStreamComboBox(self):
        for key in slef.__data.keys():
            self.__streamComboBox.addItem(key)

    def initialStreamData(self):

        # get all features
        for feature in self.__layer.getFeatures():

            try:

                # get basic properties
                id = feature["id"]
                profile = feature["profile"]
                referentId = feature["ReferentId"]
                distance = feature["DistanceFromReferent"]
                bottomLevel = min(profile, key=lambda x: x[1])[1]

                # get profile leveling
                sortedProfile = sorted(profile, key=lambda x: x[0])
                minY = sortedProfile[0][0]
                maxY = sortedProfile[-1][0]
                midY = (minY + maxY)/2

                # get left/right highest level
                leftHight = max(
                    filter(lambda x: x[0] < midY, profile), key=lambda x: x[1])[1]
                rightHight = max(
                    filter(lambda x: x[0] > midY, profile), key=lambda x: x[1])[1]

                # check the data is empty with referntId
                temptStreamArray = []
                if referentId not in self.__data:
                    temptStreamArray = self.__data[referentId]

                # add to temptArray
                temptStreamArray.append({
                    "id": id,
                    "leftHight": leftHight,
                    "rightHight": rightHight,
                    "bottom": bottomLevel,
                    "distance": distance
                })

            except:
                traceback.print_exc()   
    
    
    
    # QgisLayer selection
    def selectFeature(self, referentId, crossSectionId):

        # select only active crossSection
        activeExpression = "\"ReferentId\" = \'" + referentId + \
            "\' and \"id\" = \'" + crossSectionId + "\'"
        activeCrossSection = self.__layer.getFeatures(
            QgsFeatureRequest(QgsExpression(activeExpression)))
        
        # select referent stream without active crossSection
        referentExpression = "\"ReferentId\" = \'" + referentId + \
            "\' and \"id\" != \'" + crossSectionId + "\'"
        referentCrossSection = self.__layer.getFeatures(
            QgsFeatureRequest(QgsExpression(referentExpression)))
        
        # merge these two
        activeIds = [i.id() for i in activeCrossSection]
        referentIds =  [i.id() for i in referentCrossSection]
        selectedIds = activeIds + referentIds
        
        # selected
        self.__layer.select(selectedIds)