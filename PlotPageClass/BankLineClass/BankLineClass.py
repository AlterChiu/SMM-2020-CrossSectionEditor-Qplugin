import pyqtgraph as pyqtgraph
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QComboBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsWkbTypes, QgsProcessingUtils, QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem, QgsFeatureRequest,QgsExpression

from .PlotBankLevelWidgetClass import PlotBankLevelWidgetClass
import requests
import traceback
import json

import sys


class BankLineClass:
    def __init__(self, dlg, selectedLayer):

        # initial page
        self.__dlg = dlg
        self.__layer = selectedLayer

        # plotPoage
        self.__currentSelection = {
            "activeIndex": 0,
            "hoverIndex": None
        }

        # initial button
        self.__leftButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "bankLineSelectionLeft")
        self.__leftButton.clicked.connect(lambda: self.__selectionGoLeft())

        self.__rightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "bankLineSelectionRight")
        self.__rightButton.clicked.connect(lambda: self.__selectionGoRight())

        self.__selectButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "bankLineSelection")
        self.__selectButton.clicked.connect(lambda: self.__select())

        self.__plotButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "bankLineSelectionPlot")
        self.__plotButton.clicked.connect(lambda: self.__plot())

        # initial plotWidget
        self.__plotWidget = self.__dlg.findChild(
            pyqtgraph.PlotWidget, "bankLineSelectionPlotWidget")
        self.__plotClass = PlotBankLevelWidgetClass(self.__plotWidget)

    # datas
        # # "collected by referntId"
        # referentId :

        # # sorted by distance
        # [
        #     {
        #         id: id,
        #         leftHight : "the highest level of the left crossSection",
        #         rightHight : "the highest level of the right crossSection",
        #         bottom : "the lowest level of the crossSection",
        #         distance : "distance from begining"
        #     }
        # ]
    def __initialStreamData(self, selectedReferentID) -> list:
        data = []

        # get all features
        for feature in self.__layer.getFeatures():
            try:
                referentId = feature["ReferentId"]
                if referentId == selectedReferentID:

                    # get basic properties
                    id = feature["id"]
                    profile = eval(feature["profile"])
                    distance = feature["DistanceFromReferent"]
                    bottomLevel = min(profile, key=lambda x: float(x[1]))[1]

                    # get profile leveling
                    sortedProfile = sorted(profile, key=lambda x: x[0])
                    minY = float(sortedProfile[0][0])
                    maxY = float(sortedProfile[-1][0])
                    midY = (minY + maxY)/2

                    # get left/right highest level
                    leftHight = max(
                        filter(lambda x: float(x[0]) < midY, profile), key=lambda x: x[1])[1]
                    rightHight = max(
                        filter(lambda x: float(x[0]) > midY, profile), key=lambda x: x[1])[1]

                    # add to temptArray
                    data.append({
                        "id": id,
                        "leftHight": leftHight,
                        "rightHight": rightHight,
                        "bottomHight": bottomLevel,
                        "distance": distance
                    })

            except:
                traceback.print_exc()

        # sort the data
        return sorted(data, key=lambda x: x["distance"])

    def initialCurrentSelection(self):
        self.__currentSelection = {
            "activeIndex": 0,
            "hoverIndex": None
        }

    # button for plot
    # ===================================================================

    def __plot(self):
        # clear
        self.initialCurrentSelection()

        # get selectedFeature
        try:
            features = list(self.__layer.selectedFeatures())
            selectedFeature = features[0]

            # get selected streamName
            streamName = selectedFeature["ReferentId"]
            streamData = self.__initialStreamData(streamName)

            # select all crossSection on this stream
            self.selectFeatureID(streamName, selectedFeature["id"])
            self.__plotClass.plot(streamName, streamData)

        except:
            traceback.print_exc()
            print("no selected feature to plot bankLine")

    # button for slelctions
    # ===================================================================

    def __select(self):
        currentHoverIndex = self.__currentSelection["hoverIndex"]
        if currentHoverIndex != None:

            # get id from plotWidget by index
            selectId = self.__plotClass.getSelectedId(currentHoverIndex)
            referentId = self.__plotClass.getReferentId()

            if selectedID != None and referentId != None:

                # plot widget
                self.__plotClass.plotActive(currentHoverIndex)
                self.__plotClass.clearHover()

                # modify privat constant
                self.selectFeatureID(referentId, selectId)
                self.__currentSelection["activeIndex"] = currentHoverIndex
                self.__currentSelection["activeIndex"] = self.__currentSelection["hoverIndex"]

    def __selectionGoLeft(self):
        currentHoverIndex = self.__currentSelection["hoverIndex"]
        if currentHoverIndex == None:
            currentHoverIndex = self.__currentSelection["activeIndex"]

        nextHoverIndex = currentHoverIndex-1
        if nextHoverIndex >= 0:
            self.__plotClass.plotHover(nextHoverIndex)
            self.__currentSelection["hoverIndex"] = nextHoverIndex

    def __selectionGoRight(self):
        currentHoverIndex = self.__currentSelection["hoverIndex"]
        if currentHoverIndex == None:
            currentHoverIndex = self.__currentSelection["activeIndex"]

        nextHoverIndex = currentHoverIndex+1
        if nextHoverIndex < self.__plotClass.getCrossSectionSize():
            self.__plotClass.plotHover(nextHoverIndex)
            self.__currentSelection["hoverIndex"] = nextHoverIndex

    # QgisLayer selection
    def selectFeatureID(self, referentId, crossSectionId):

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
        referentIds = [i.id() for i in referentCrossSection]
        selectedIds = activeIds + referentIds

        # selected
        self.__layer.select(selectedIds)

    def selectedReferentID(self, referentId):

        # select referent stream without active crossSection
        referentExpression = "\"ReferentId\" = \'" + referentId + "\'"
        self.__layer.selectByExpression(referentExpression)
