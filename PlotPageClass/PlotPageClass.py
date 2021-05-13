# pyqt py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QComboBox

# qgis py
from qgis.gui import QgsFileWidget
from qgis.core import QgsWkbTypes, QgsPointXY, QgsRaster, QgsFeatureRequest
from qgis.utils import iface
import pyqtgraph as pyqtgraph
import json

# system py
import math
import sys
import requests

# userCreate py
from .PlotWidget.PlotWidgetClass import PlotWidgetClass
from .TableWidget.TableWidgeClass import TableWidgeClass
from .ModifyButton.ModifyButton import ModifyButtonClass
from .FixPointClass import FixPointClass

from .ApiRequest.DemLevel import DemLevel
from .ApiRequest.Update import Update
from .ApiRequest.Create import Create
from .ApiRequest.Delete import Delete
from .BankLineClass.BankLineClass import BankLineClass
from .plugins.SimilarityClass import SimilarityClass

import traceback


class PlotPageClass:

    def __init__(self, dlg, firstPageClass):

     # constant
        self.__rasterDetectLength = 1
        self.__rasterReplaceResolution = self.__rasterDetectLength
        self.__nullValue = -999.0

     # get dlg
        self.__dlg = dlg

     # get object in plot page

        # plot widget
        self.__plotWidget = self.__dlg.findChild(
            pyqtgraph.PlotWidget, "plotWidget")
        self.__plotClass = PlotWidgetClass(self.__plotWidget)

        # table widget
        self.__editTable = self.__dlg.findChild(
            QtWidgets.QTableWidget, "editTableWidget")
        self.__tableClass = TableWidgeClass(self.__editTable, self.__plotClass)

        # fix point widget
        self.__currentDemPoints = []  # [[x,y,l,z]...]
        self.__demFixPointsWidget = FixPointClass(
            dlg, prefixName="dem", plotWidget=self.__plotClass, dataList=self.__currentDemPoints)

        self.__sbkFixPointsWidget = FixPointClass(
            dlg, prefixName="sbk", plotWidget=self.__plotClass, dataList=self.__tableClass.getTableValues())

        # modify buttons
        self.__modifyButtons = ModifyButtonClass(dlg, self.__tableClass)

        # set crossSection plot widget lable
        self.__crossSectionSbkLable = self.__dlg.findChild(
            QtWidgets.QLabel, "CrossSectionSbkLable")
        self.__crossSectionSbkLable.setStyleSheet("color : blue")

        self.__crossSectionDemLable = self.__dlg.findChild(
            QtWidgets.QLabel, "CrossSectionDemLable")
        self.__crossSectionDemLable.setStyleSheet("color : red")

        # set bankLine plot widget lable
        self.__bankLineLeftLable = self.__dlg.findChild(
            QtWidgets.QLabel, "BankLineLeftLable")
        self.__bankLineLeftLable.setStyleSheet("color : green")

        self.__bankLineRightLable = self.__dlg.findChild(
            QtWidgets.QLabel, "BankLineRightLable")
        self.__bankLineRightLable.setStyleSheet("color : pink")

        self.__bankLineBottomLable = self.__dlg.findChild(
            QtWidgets.QLabel, "BankLineBottomLable")
        self.__bankLineBottomLable.setStyleSheet("color : blue")

        self.__saveButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "saveButton")
        self.__saveButton.clicked.connect(lambda: self.__save())

        self.__restoreButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "restoreButton")
        self.__restoreButton.clicked.connect(lambda: self.__restore())

        self.__replaceButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "replaceButton")
        self.__replaceButton.clicked.connect(
            lambda: self.__replace(resolution=self.__rasterReplaceResolution))

        self.__replaceLeftButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "replaceLeftButton")
        self.__replaceLeftButton.clicked.connect(
            lambda: self.__replaceLeft())

        self.__replaceRightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "replaceRightButton")
        self.__replaceRightButton.clicked.connect(
            lambda: self.__replaceRight())

        self.__replaceMidButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "replaceMidButton")
        self.__replaceMidButton.clicked.connect(
            lambda: self.__replaceMid())

        self.__addRowButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "addRowButton")
        self.__addRowButton.clicked.connect(lambda: self.__addRow())

        self.__deleteRowButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "deleteRowButton")
        self.__deleteRowButton.clicked.connect(lambda: self.__deleteRow())

        self.__replaceResolutionUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "replaceResolutionUpButton")
        self.__replaceResolutionUpButton.clicked.connect(
            lambda: self.__replaceResolutionUp())

        self.__replaceResolutionDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "replaceResolutionDownButton")
        self.__replaceResolutionDownButton.clicked.connect(
            lambda: self.__replaceResolutionDown())

        self.__similiarScore = self.__dlg.findChild(
            QtWidgets.QLabel, "similiarScore")

     # getting parameter from first page
        self.__demLayer = firstPageClass.getDemLayer()
        self.__splitLineLayer = firstPageClass.getSplitLineLayer()
        self.__editCounty = firstPageClass.getEditorCounty()

     # create bankLine leveing plotwidget
        self.__bankLineClass = BankLineClass(self.__dlg, self.__splitLineLayer)

     # detect if selected geometry onchange
        # """
        self.__splitLineLayer.startEditing()
        self.__splitLineLayer.selectionChanged.connect(
            self.__reFreshPlotWidget)
        self.__splitLineLayer.geometryChanged.connect(
            self.__reFreshPlotWidget)
        # """

        # detect if selected layer add new feature
        self.__splitLineLayer.featureAdded.connect(self.__featureAdd)
        self.__splitLineLayer.featureDeleted.connect(self.__featureDelete)
    # dialog functions
    # -----------------------------------------------------------

    def __featureAdd(self, fId):

        # disconnect selection
        self.__splitLineLayer.selectionChanged.disconnect(
            self.__reFreshPlotWidget)

        # select feature
        self.__splitLineLayer.removeSelection()
        self.__splitLineLayer.select(fId)
        try:
            features = list(self.__splitLineLayer.selectedFeatures())
            selectedFeature = features[0]

        # get selected geometry
            geometry = selectedFeature.geometry()
            temptVertices = list(geometry.vertices())

        # get feature properties
            # startPoint
            startPoint = [temptVertices[0].x(), temptVertices[0].y()]

            # endPoint
            endPoint = [temptVertices[1].x(), temptVertices[1].y()]

            # profile
            demPoints = DemLevel.getRasterValue(geometry)
            profile = list(
                map(lambda point: [point["dy"], point["z"]], demPoints))

        # update to webservice
            newID = Create.createCrossSection(
                startPoint, endPoint, profile, self.__editCounty)

        # change attribute table

            # startPoint
            startPointTid = selectedFeature.fields().indexFromName("start-point")
            self.__splitLineLayer.changeAttributeValue(
                fId, startPointTid, str(startPoint))

            # endPoint
            endPointTid = selectedFeature.fields().indexFromName("end-point")
            self.__splitLineLayer.changeAttributeValue(
                fId, endPointTid, str(endPoint))

            # profile
            profileTid = selectedFeature.fields().indexFromName("profile")
            self.__splitLineLayer.changeAttributeValue(
                fId, profileTid, str(profile))

            # crossSectionID
            idTid = selectedFeature.fields().indexFromName("id")
            self.__splitLineLayer.changeAttributeValue(
                fId, idTid, newID)

        # remove selection feature
            self.__splitLineLayer.removeSelection()

            print("feature create")
        except:

            traceback.print_exc()
            print("create fail")

        # reconnect selectionChange method
        print("connect")
        self.__splitLineLayer.selectionChanged.connect(
            self.__reFreshPlotWidget)

        try:
            self.__splitLineLayer.select(fId)
        except:
            pass

    def __featureDelete(self, fId):
        feature = list(self.__splitLineLayer.dataProvider().getFeatures(
            QgsFeatureRequest([fId])))[0]

        deletedCrossSectionId = feature["id"]
        print(deletedCrossSectionId)
        Delete.deleteCrossSection(self.__editCounty, deletedCrossSectionId)

    def __restore(self):
        self.__reFreshPlotWidget()

    def __replace(self, resolution: float, minL: float = -1*float("inf"), maxL: float = float("inf")):
        try:
            features = list(self.__splitLineLayer.selectedFeatures())

            # get values from tables
            # data format : [[x,y,l,z]....]
            tableValues = list(filter(
                lambda point: point[2] < minL or point[2] > maxL, self.__tableClass.getTableValues()))

            # get values from demLevel
            # data format : [{"x":x , "y":y , "dy" :dy ,"z":z}]
            xyzList = DemLevel.wrapXYZResolution(
                list(map(lambda point: {"x": point[0], "y": point[1], "dy": point[2], "z": point[3]},
                         self.__currentDemPoints)), resolution=resolution/2.0)

            # normalize currentDemPoints by dy
            maxDy = max(self.__currentDemPoints, key=lambda point: point[2])[2]
            minDy = min(self.__currentDemPoints, key=lambda point: point[2])[2]
            midDy = (maxDy + minDy)/2

            # out
            for point in xyzList:

                normalizeDy = point["dy"]-midDy
                if normalizeDy > minL and normalizeDy < maxL:
                    tableValues.append(
                        [point["x"], point["y"], normalizeDy, point["z"]])

            self.__tableClass.replace(sorted(tableValues, key=lambda x: x[2]))
        except:
            traceback.print_exc(file=sys.stdout)
            print("replace error")

    def __replaceLeft(self):
        try:
            maxL = float(self.__sbkFixPointsWidget.getLeftFixPoint()[0])
            minL = float(self.__demFixPointsWidget.getLeftFixPoint()[0])
            self.__replace(
                resolution=self.__rasterReplaceResolution, minL=minL, maxL=maxL)
        except:
            traceback.print_exc()
            pass

    def __replaceRight(self):
        try:
            minL = float(self.__sbkFixPointsWidget.getRightFixPoint()[0])
            maxL = float(self.__demFixPointsWidget.getRightFixPoint()[0])
            self.__replace(
                resolution=self.__rasterReplaceResolution, minL=minL, maxL=maxL)
        except:
            traceback.print_exc()
            pass

    def __replaceMid(self):
        try:
            minL = float(self.__sbkFixPointsWidget.getLeftFixPoint()[0])
            maxL = float(self.__sbkFixPointsWidget.getRightFixPoint()[0])
            self.__replace(
                resolution=self.__rasterReplaceResolution, minL=minL, maxL=maxL)
        except:
            pass

    def __addRow(self):
        self.__tableClass.addNewRow()

    def __deleteRow(self):
        self.__tableClass.deletSelectedRow()

    def __rationTRUp(self):
        self.__tableClass.dataMove(
            ratioL=1.0, moveL=0.1, directionL=1, ratioZ=1.0, moveZ=0.1, directionZ=1)

    def __replaceResolutionUp(self):
        if(self.__rasterReplaceResolution + 1 < 50.0):
            self.__rasterReplaceResolution = self.__rasterReplaceResolution + 1
        else:
            self.__rasterReplaceResolution = self.__rasterDetectLength
        self.__replace(resolution=self.__rasterReplaceResolution)

    def __replaceResolutionDown(self):
        if(self.__rasterReplaceResolution - 1 < self.__rasterDetectLength):
            self.__rasterReplaceResolution = 50.0
        else:
            self.__rasterReplaceResolution = self.__rasterReplaceResolution - 1
        self.__replace(resolution=self.__rasterReplaceResolution)

    def __save(self):
        try:
            # get selected feature
            selectedFeature = list(self.__splitLineLayer.selectedFeatures())[0]
            featureID = selectedFeature["id"]

            # get table data
            tableData = self.__tableClass.getTableValues()

            # get startPoint and endPoint, [x,y,z]
            startPoint = self.__tableClass.getStartPoint()
            endPoint = self.__tableClass.getEndPoint()

            # get fixPoints
            # [y,z]
            leftFixPoint = self.__sbkFixPointsWidget.getLeftFixPoint()
            # [y,z]
            rightFixPoint = self.__sbkFixPointsWidget.getRightFixPoint()

            # save
            updateDate = {
                "id": featureID,
                "tableData": tableData,
                "startPoint": startPoint,
                "endPoint": endPoint,
                "leftFixPoint": leftFixPoint,
                "rightFixPoint": rightFixPoint,
                "countyId": self.__editCounty
            }
            Update.crossSection(updateDate, selectedFeature,
                                self.__splitLineLayer)

        except:
            traceback.print_exc()

    # plot widget
    # ------------------------------------------------------------
    def __reFreshPlotWidget(self):
        # clear plot widge
        self.__clearPlotPage()
        self.__currentDemPoints.clear()
        self.__similiarScore.setText("0")

        # get geometry
        featureList = []
        selectedFeature = None
        selectedGeometryYZ = None
        currentSelectedGeometryID = None
        try:
            features = list(self.__splitLineLayer.selectedFeatures())
            selectedFeature = features[0]
            for featureIndex in range(0, 10):
                featureList.append(features[featureIndex])
        except:
            print("select" + str(len(featureList)))

        # start plotting
        if len(featureList) > 0:

            # plot primary line
            demPoints = DemLevel.getRasterValue(featureList[0].geometry())
            for point in demPoints:
                self.__currentDemPoints.append(
                    [point["x"], point["y"], point["dy"], point["z"]])

            # normalize currentDemPoints by dy
            maxDy = max(self.__currentDemPoints, key=lambda point: point[2])[2]
            minDy = min(self.__currentDemPoints, key=lambda point: point[2])[2]
            midDy = round((maxDy + minDy)/2, 2)
            for point in self.__currentDemPoints:
                point[2] = point[2] - midDy

            # data format : [[x,y,z]....]
            geometryValueList = list(
                map(lambda point: [point[2], point[3]], self.__currentDemPoints))
            self.__plotClass.addDataPrimary(geometryValueList)

            # plot similiarScore
            similiareScor = SimilarityClass(selectedFeature, list(map(
                lambda point: [point["dy"], point["z"]], demPoints)))
            self.__similiarScore.setText(
                str(similiareScor.SimilarityCompare()))

        # plot sbkCrossSection
            self.__plotSBK(selectedFeature)

        # plot fixPoint
            self.__plotDemFixPoint(geometryValueList)

        # plot otherLine
        if len(featureList) > 1:

            # plot line from hyDem raster
            for index in range(1, len(featureList)):

                # parse json formate to data format
                # data format : [[x1,y1],[x2,y2]....[xn,yn]]
                yzLine = json.loads(featureList[index]["profile"])
                self.__plotClass.addDataSecondary(yzLine)

                # normalize the yzLine, to make centerX to 0
                # data format : [[[x1,x2...xn] , [y1,y2.....yn]]]
                yzLine = self.__plotClass.dataNormalize(yzLine)

        # set title
        try:
            self.__plotClass.setTitle(selectedFeature["id"])
        except:
            self.__plotClass.setTitle("no sbk selected")

        # plot on widget
        self.__plotClass.plotPrimary()
        self.__plotClass.plotSecondary()

    # plot SBK
    def __plotSBK(self, selectedFeature):
        # add data to tableWidget and plot line
        try:
            # parse json formate to data format
            # data format : [[x1,y1],[x2,y2]....[xn,yn]]
            yzLine = json.loads(selectedFeature["profile"])

            # normalize the yzLine, to make centerX to 0
            # data format : [[x1...xn] , [y1....yn]]
            yzLine = self.__plotClass.dataNormalize(yzLine)

            # plot fixPoint
            self.__sbkFixPointsWidget.setLeftFixPointYZ(
                round(yzLine[0][0], 2), round(yzLine[1][0], 2))
            self.__sbkFixPointsWidget.setRightFixPointYZ(
                round(yzLine[0][-1], 2), round(yzLine[1][-1], 2))
            self.__sbkFixPointsWidget.plot()
            self.__sbkFixPointsWidget.unBlockTextEdit()

            # add to tableWidget
            # -------------------------------------------------
            verticeList = list(selectedFeature.geometry().vertices())

            # add startPoint
            startX = verticeList[0].x()
            startY = verticeList[0].y()
            startZ = DemLevel.getPointZValue(startX, startY)
            if startZ == self.__nullValue:
                startZ = 0.0

            self.__tableClass.setStartPoint(startX, startY, startZ)

            # add endPoint
            endX = verticeList[-1].x()
            endY = verticeList[-1].y()
            endZ = DemLevel.getPointZValue(endX, endY)

            if startZ == self.__nullValue:
                endZ = 0.0

            self.__tableClass.setEndPoint(endX, endY, endZ)

            # add other points
            yList = yzLine[0]
            zList = yzLine[1]

            for index in range(0, len(yList)):
                self.__tableClass.addPoint(yList[index], zList[index])

            # reload table
            self.__tableClass.reload()

        except:
            traceback.print_exc()
            print("error table create faild")

        # -----------------------------------READ RASTER VALUE FROM DEMLAYER------------------------------------
        # try:
        # res = self.__demLayer.dataProvider().identify(QgsPointXY(x , y), QgsRaster.IdentifyFormatValue).results()
        # return res[1]
        # except:
        # return self.__nullValue

    # plot dem fixPoint
    def __plotDemFixPoint(self, geometryValueList):
        normolizeVlaueList = self.__plotClass.dataNormalize(
            geometryValueList)
        yList = normolizeVlaueList[0]
        zList = normolizeVlaueList[1]

        # detected from y=0 , find the higest point for each side
        leftY = None
        leftZ = -math.inf

        rightY = None
        rightZ = -math.inf

        for index in range(0, len(yList)):  # point=[y,z]
            if yList[index] < 0 and zList[index] > leftZ:
                leftY = yList[index]
                leftZ = zList[index]

            elif yList[index] > 0 and zList[index] > rightZ:
                rightY = yList[index]
                rightZ = zList[index]
        try:

            self.__demFixPointsWidget.setLeftFixPointYZ(
                round(leftY, 2), round(leftZ, 2))
            self.__demFixPointsWidget.setRightFixPointYZ(
                round(rightY, 2), round(rightZ, 2))
            self.__demFixPointsWidget.plot()
            self.__demFixPointsWidget.unBlockTextEdit()
        except:
            traceback.print_exc()

    # clear plotPage
    def __clearPlotPage(self):
        self.__plotClass.clear()
        self.__rasterReplaceResolution = self.__rasterDetectLength

        # clear fixPoint widget
        self.__sbkFixPointsWidget.clear()
        self.__sbkFixPointsWidget.blockTextEdit()

    # -------------------------------------READ RASTER PIXEL FROM FROM DEMLAYER----------------------------------
    # def __getRasterSize(self):
    #   pixelX = self.__demLayer.rasterUnitsPerPixelX()
    #   pixelY = self.__demLayer.rasterUnitsPerPixelY()
    #   return math.sqrt(pow(pixelX, 2) + pow(pixelY, 2))
