# pyqt py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QComboBox

# qgis py
from qgis.gui import QgsFileWidget
from qgis.core import QgsWkbTypes, QgsPointXY, QgsRaster
from qgis.utils import iface
import pyqtgraph as pyqtgraph
import json

# system py
import math
import sys
import requests

# userCreate py
from .PlotWidgetClass import PlotWidgetClass
from .TableWidgeClass import TableWidgeClass
from .FixPointClass import FixPointClass

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

        # fix point widget
        self.__fixPointsWidget = FixPointClass(dlg, self.__plotClass)

        # table widget
        self.__editTable = self.__dlg.findChild(
            QtWidgets.QTableWidget, "editTableWidget")
        self.__tableClass = TableWidgeClass(self.__editTable, self.__plotClass)

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

        self.__addRowButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "addRowButton")
        self.__addRowButton.clicked.connect(lambda: self.__addRow())

        self.__deleteRowButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "deleteRowButton")
        self.__deleteRowButton.clicked.connect(lambda: self.__deleteRow())

        self.__moveUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveUpButton")
        self.__moveUpButton.clicked.connect(lambda: self.__moveUp())

        self.__moveDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveDownButton")
        self.__moveDownButton.clicked.connect(lambda: self.__moveDown())

        self.__moveRightButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveRightButton")
        self.__moveRightButton.clicked.connect(lambda: self.__moveRight())

        self.__moveLeftButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveLeftButton")
        self.__moveLeftButton.clicked.connect(lambda: self.__moveLeft())

        self.__ratioTopOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioTopOutButton")
        self.__ratioTopOutButton.clicked.connect(lambda: self.__ratioTopOut())

        self.__ratioTopInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioTopInButton")
        self.__ratioTopInButton.clicked.connect(lambda: self.__ratioTopIn())

        self.__ratioBottomOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBottomOutButton")
        self.__ratioBottomOutButton.clicked.connect(
            lambda: self.__ratioBottomOut())

        self.__ratioBottomInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioBottomInButton")
        self.__ratioBottomInButton.clicked.connect(
            lambda: self.__ratioBottomIn())

        self.__ratioRightInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioRightInButton")
        self.__ratioRightInButton.clicked.connect(
            lambda: self.__ratioRightIn())

        self.__ratioRightOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioRightOutButton")
        self.__ratioRightOutButton.clicked.connect(
            lambda: self.__ratioRightOut())

        self.__ratioLeftOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioLeftOutButton")
        self.__ratioLeftOutButton.clicked.connect(
            lambda: self.__ratioLeftOut())

        self.__ratioLeftInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "ratioLeftInButton")
        self.__ratioLeftInButton.clicked.connect(lambda: self.__ratioLeftIn())

        self.__moveTopOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveTopOutButton")
        self.__moveTopOutButton.clicked.connect(lambda: self.__moveTopOut())

        self.__moveTopInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveTopInButton")
        self.__moveTopInButton.clicked.connect(lambda: self.__moveTopIn())

        self.__moveBottomOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBottomOutButton")
        self.__moveBottomOutButton.clicked.connect(
            lambda: self.__moveBottomOut())

        self.__moveBottomInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveBottomInButton")
        self.__moveBottomInButton.clicked.connect(
            lambda: self.__moveBottomIn())

        self.__moveRightInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveRightInButton")
        self.__moveRightInButton.clicked.connect(lambda: self.__moveRightIn())

        self.__moveRightOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveRightOutButton")
        self.__moveRightOutButton.clicked.connect(
            lambda: self.__moveRightOut())

        self.__moveLeftOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveLeftOutButton")
        self.__moveLeftOutButton.clicked.connect(lambda: self.__moveLeftOut())

        self.__moveLeftInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "moveLeftInButton")
        self.__moveLeftInButton.clicked.connect(lambda: self.__moveLeftIn())

        self.__zoomInButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "zoomInButton")
        self.__zoomInButton.clicked.connect(lambda: self.__zoomIn())

        self.__zoomOutButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "zoomOutButton")
        self.__zoomOutButton.clicked.connect(lambda: self.__zoomOut())

        self.__replaceResolutionUpButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "replaceResolutionUpButton")
        self.__replaceResolutionUpButton.clicked.connect(
            lambda: self.__replaceResolutionUp())

        self.__replaceResolutionDownButton = self.__dlg.findChild(
            QtWidgets.QPushButton, "replaceResolutionDownButton")
        self.__replaceResolutionDownButton.clicked.connect(
            lambda: self.__replaceResolutionDown())

     # getting parameter from first page
        self.__demLayer = firstPageClass.getDemLayer()
        self.__splitLineLayer = firstPageClass.getSplitLineLayer()
        self.__editCounty = firstPageClass.getEditorCounty()

     # detect if selected geometry onchange
        # """
        self.__splitLineLayer.startEditing()
        self.__splitLineLayer.selectionChanged.connect(
            lambda: self.__reFreshPlotWidget())
        self.__splitLineLayer.geometryChanged.connect(
            lambda: self.__reFreshPlotWidget())
        # """

    # dialog functions
    # -----------------------------------------------------------
    def __save(self):

        try:
            # get selected feature
            selectedFeature = list(self.__splitLineLayer.selectedFeatures())[0]
            featureID = selectedFeature["id"]

            # get table data
            tableData = self.__tableClass.getTableValues()

            # get startPoint and endPoint, [x,y,z]
            startPoint = self.__tableClass.getStartPoint()
            startPoint[2] = self.__getPointZValue(startPoint[0], startPoint[1])

            endPoint = self.__tableClass.getEndPoint()
            endPoint[2] = self.__getPointZValue(endPoint[0], endPoint[1])

            # get boundary length
            maxLength = math.sqrt(
                pow(startPoint[0] - endPoint[0], 2) + pow(startPoint[1] - endPoint[1], 2))

            # create output profile
            outProfile = []

            # get fixPoints
            leftFixPoint = self.__fixPointsWidget.getLeftFixPoint()  # [y,z]
            rightFixPoint = self.__fixPointsWidget.getRightFixPoint()  # [y,z]

            # add left fix(boundary) point
            outProfile.append(leftFixPoint)

            # add other points which within the boundary
            for rowData in tableData:  # [x,y,l,z]
                if rowData[2] > leftFixPoint[0] and rowData[2] < rightFixPoint[0]:
                    outProfile.append([rowData[2], rowData[3]])

            # add end point
            outProfile.append(rightFixPoint)

            # update to rest-api (patch)
            data = {"startPoint": startPoint,
                    "endPoint": endPoint, "profile": outProfile}
            header = {"content-type": "application/json"}
            request = requests.patch("https://h2-demo.pointing.tw/api/cross-sections/" +
                                     self.__editCounty + "/" + featureID, data=json.dumps(data), headers=header)
            print(request.text)

            # new id
            newID = "X" + str(int((startPoint[0] + endPoint[0])/2)) + \
                "-Y" + str(int((startPoint[1] + endPoint[1])/2))

            # commit to layer
            selectedFeature["id"] = newID
            selectedFeature["profile"] = str(outProfile)
            self.__splitLineLayer.updateFeature(selectedFeature)

        except:
            traceback.print_exc()
            Exception("save error")

    def __restore(self):
        self.__reFreshPlotWidget()

    def __replace(self, resolution: float):
        try:
            features = list(self.__splitLineLayer.selectedFeatures())
            xyzList = self.__getRasterValuesXYZ(
                features[0].geometry(), resolution=resolution)
            self.__tableClass.replace(xyzList)
        except:
            traceback.print_exc(file=sys.stdout)
            print("replace error")

    def __addRow(self):
        self.__tableClass.addNewRow()

    def __deleteRow(self):
        self.__tableClass.deletSelectedRow()

    def __moveUp(self):
        self.__tableClass.dataMove(moveZ=0.1)

    def __moveDown(self):
        self.__tableClass.dataMove(moveZ=-0.1)

    def __moveRight(self):
        self.__tableClass.dataMove(moveL=1.0)

    def __moveLeft(self):
        self.__tableClass.dataMove(moveL=-1.0)

    def __ratioTopOut(self):
        self.__tableClass.topDataMove(ratio=0.15)

    def __ratioTopIn(self):
        self.__tableClass.topDataMove(ratio=-0.15)

    def __ratioBottomOut(self):
        self.__tableClass.bottomDataMove(ratio=0.15)

    def __ratioBottomIn(self):
        self.__tableClass.bottomDataMove(ratio=-0.15)

    def __ratioRightOut(self):
        self.__tableClass.rightDataMove(ratio=0.15)

    def __ratioRightIn(self):
        self.__tableClass.rightDataMove(ratio=-0.15)

    def __ratioLeftOut(self):
        self.__tableClass.leftDataMove(ratio=0.15)

    def __ratioLeftIn(self):
        self.__tableClass.leftDataMove(ratio=-0.15)

    def __moveTopOut(self):
        self.__tableClass.topDataMove(moveZ=0.1)

    def __moveTopIn(self):
        self.__tableClass.topDataMove(moveZ=-0.1)

    def __moveBottomOut(self):
        self.__tableClass.bottomDataMove(moveZ=-0.1)

    def __moveBottomIn(self):
        self.__tableClass.bottomDataMove(moveZ=1.0)

    def __moveRightOut(self):
        self.__tableClass.rightDataMove(moveL=1.0)

    def __moveRightIn(self):
        self.__tableClass.rightDataMove(moveL=-1.0)

    def __moveLeftOut(self):
        self.__tableClass.leftDataMove(moveL=-1.0)

    def __moveLeftIn(self):
        self.__tableClass.leftDataMove(moveL=1.0)

    def __zoomOut(self):
        self.__tableClass.dataZoom(0.95)

    def __zoomIn(self):
        self.__tableClass.dataZoom(1.05)

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

    # plot widget
    # ------------------------------------------------------------
    def __reFreshPlotWidget(self):
        # clear plot widge
        self.__plotClass.clear()
        self.__rasterReplaceResolution = self.__rasterDetectLength

        # clear fixPoint widget
        self.__fixPointsWidget.clear()
        self.__fixPointsWidget.blockTextEdit()

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

        # plot primary
        if len(featureList) > 0:
            # plot primary line
            geometryValueList = self.__getRasterValuesYZ(
                featureList[0].geometry(), self.__rasterReplaceResolution)
            self.__plotClass.addDataPrimary(geometryValueList)

        # plot sbkCrossSection
            self.__plotSBK(selectedFeature)

        # plot fixPoint
            # make geometryValueList to center 0(normolize)
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

                self.__fixPointsWidget.setLeftFixPointYZ(
                    round(leftY, 2), round(leftZ, 2))
                self.__fixPointsWidget.setRightFixPointYZ(
                    round(rightY, 2), round(rightZ, 2))
                self.__fixPointsWidget.plot()
                self.__fixPointsWidget.unBlockTextEdit()
            except:
                traceback.print_exc()

        # plot otherLine
        if len(featureList) > 1:

            # plot line from hyDem raster
            for index in range(1, len(featureList)):

                # parse json formate to data format
                # data format : [[x1,y1],[x2,y2]....[xn,yn]]
                yzLine = json.loads(featureList[index]["profile"])

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
            # data format : [[[x1,x2...xn] , [y1,y2.....yn]]]
            yzLine = self.__plotClass.dataNormalize(yzLine)

            # add to tableWidget
            # -------------------------------------------------
            verticeList = list(selectedFeature.geometry().vertices())

            # add startPoint
            startX = verticeList[0].x()
            startY = verticeList[0].y()
            startZ = self.__getPointZValue(startX, startY)
            if startZ == self.__nullValue:
                startZ = 0.0

            self.__tableClass.setStartPoint(startX, startY, startZ)

            # add endPoint
            endX = verticeList[-1].x()
            endY = verticeList[-1].y()
            endZ = self.__getPointZValue(endX, endY)
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

    # get Raster layer properties
    def __getRasterValuesYZ(self, geometry, resolution: float) -> list:

        requestPoints = self.__getRasterValue(geometry, resolution)
        outList = []

        for point in requestPoints:
            outList.append([point["dy"], point["z"]])

        return outList

    # get Raster layer properties
    def __getRasterValuesXYZ(self, geometry, resolution: float):

        requestPoints = self.__getRasterValue(geometry, resolution)
        outList = []

        for point in requestPoints:
            outList.append([point["x"], point["y"], point["z"]])

        return outList

    # return api request profile = profile:[{x,y,dy,z}....]
    def __getRasterValue(self, geometry, resolution: float) -> list:

        # get vertice from geometry
        temptVertices = list(geometry.vertices())
        startPoint = [temptVertices[0].x(), temptVertices[0].y()]
        endPoint = [temptVertices[-1].x(), temptVertices[-1].y()]

        length = pow(pow(startPoint[0] - endPoint[0], 2) +
                     pow(startPoint[1] - endPoint[1], 2), 0.5)
        disX = endPoint[0] - startPoint[0]
        disY = endPoint[1] - startPoint[1]

        # create api request parameters
        try:
            pointJson = {
                "type": "Lintstring", "coordinates": [startPoint, endPoint]
            }
            header = {"content-type": "application/json"}
            request = requests.post(
                "https://h2-demo.pointing.tw/service/dem/profile?resolution=1", data=json.dumps(pointJson), headers=header)

            # request jsonObject
            requestJson = json.loads(request.text)

            # classify request by dy(key) and z(value list)
            yzList = {}
            for point in requestJson["profile"]:
                multiple = (int)(point["dy"]/resolution)
                temptList = yzList.get(multiple, [])
                temptList.append(point["z"])
                yzList[multiple] = temptList

            # make yzList to output format [{x,y,dy,z}]
            outList = []

            # add startPoint
            outList.append(requestJson["profile"][0])

            # make classified yzList to mean value
            for key in yzList.keys():
                try:
                    sumValue = sum(yzList[key])
                    meanValue = sumValue/len(yzList[key])
                    temptX = startPoint[0] + disX*(key*resolution/length)
                    temptY = startPoint[1] + disY*(key*resolution/length)
                    temptDY = resolution*key

                    outList.append({"x": temptX, "y": temptY,
                                    "dy": temptDY, "z": meanValue})
                    print({"x": temptX, "y": temptY,
                                    "dy": temptDY, "z": meanValue})
                except:
                    traceback.print_exc()
                    pass

            # add endPoint
            outList.append(requestJson["profile"][-1])

            return outList
        except:
            # return empty json format
            traceback.print_exc()
            return [{"x": 0, "y": 0, "dy": 0, "z": 0}]

        # -----------------------------------READ RASTER VALUE FROM DEMLAYER------------------------------------
        # try:
        # res = self.__demLayer.dataProvider().identify(QgsPointXY(x , y), QgsRaster.IdentifyFormatValue).results()
        # return res[1]
        # except:
        # return self.__nullValue

    def __getPointZValue(self, x, y):

        pointJson = {
            "type": "point", "coordinates": [x, y]
        }
        header = {"content-type": "application/json"}
        request = requests.post(
            "https://h2-demo.pointing.tw/service/dem/profile?resolution=1", data=json.dumps(pointJson), headers=header)
        requestJson = json.loads(request.text)

        return requestJson["profile"][0]["z"]

    # -------------------------------------READ RASTER PIXEL FROM FROM DEMLAYER----------------------------------
    # def __getRasterSize(self):
    #   pixelX = self.__demLayer.rasterUnitsPerPixelX()
    #  pixelY = self.__demLayer.rasterUnitsPerPixelY()

    #    return math.sqrt(pow(pixelX, 2) + pow(pixelY, 2))
