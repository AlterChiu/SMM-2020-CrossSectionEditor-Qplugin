#pyqt py
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication,QPushButton,QLabel,QComboBox

#qgis py
from qgis.gui import QgsFileWidget
from qgis.core import QgsWkbTypes,QgsPointXY,QgsRaster
from qgis.utils import iface
import pyqtgraph as pyqtgraph
import json

#system py
import math
import sys

#userCreate py
from .PlotWidgetClass import PlotWidgetClass
from .TableWidgeClass import TableWidgeClass

import traceback


class PlotPageClass:
    def __init__(self , dlg, firstPageClass):

     # constant
        self.__rasterDetectLength = 0.5
        self.__rasterReplaceResolution = self.__rasterDetectLength
    
     # get dlg
        self.__dlg = dlg

     # get object in plot page
        
        # plot widget
        self.__plotWidget = self.__dlg.findChild(pyqtgraph.PlotWidget , "plotWidget")
        self.__plotClass = PlotWidgetClass(self.__plotWidget)

        # table widget
        self.__editTable = self.__dlg.findChild(QtWidgets.QTableWidget , "editTableWidget")
        self.__tableClass = TableWidgeClass(self.__editTable , self.__plotClass)


        self.__saveButton = self.__dlg.findChild(QtWidgets.QPushButton , "saveButton")
        self.__saveButton.clicked.connect(lambda:self.__save())

        self.__restoreButton = self.__dlg.findChild(QtWidgets.QPushButton , "restoreButton")
        self.__restoreButton.clicked.connect(lambda:self.__restore())

        self.__replaceButton = self.__dlg.findChild(QtWidgets.QPushButton , "replaceButton")
        self.__replaceButton.clicked.connect(lambda:self.__replace(resolution=self.__rasterReplaceResolution))

        self.__addRowButton = self.__dlg.findChild(QtWidgets.QPushButton , "addRowButton")
        self.__addRowButton.clicked.connect(lambda:self.__addRow())

        self.__deleteRowButton = self.__dlg.findChild(QtWidgets.QPushButton , "deleteRowButton")
        self.__deleteRowButton.clicked.connect(lambda:self.__deleteRow())

        self.__moveUpButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveUpButton")
        self.__moveUpButton.clicked.connect(lambda:self.__moveUp())

        self.__moveDownButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveDownButton")
        self.__moveDownButton.clicked.connect(lambda:self.__moveDown())

        self.__moveRightButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveRightButton")
        self.__moveRightButton.clicked.connect(lambda:self.__moveRight())

        self.__moveLeftButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveLeftButton")
        self.__moveLeftButton.clicked.connect(lambda:self.__moveLeft())

        self.__ratioTopOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "ratioTopOutButton")
        self.__ratioTopOutButton.clicked.connect(lambda:self.__ratioTopOut())

        self.__ratioTopInButton = self.__dlg.findChild(QtWidgets.QPushButton , "ratioTopInButton")
        self.__ratioTopInButton.clicked.connect(lambda:self.__ratioTopIn())

        self.__ratioBottomOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "ratioBottomOutButton")
        self.__ratioBottomOutButton.clicked.connect(lambda:self.__ratioBottomOut())

        self.__ratioBottomInButton = self.__dlg.findChild(QtWidgets.QPushButton , "ratioBottomInButton")
        self.__ratioBottomInButton.clicked.connect(lambda:self.__ratioBottomIn())

        self.__ratioRightInButton = self.__dlg.findChild(QtWidgets.QPushButton , "ratioRightInButton")
        self.__ratioRightInButton.clicked.connect(lambda:self.__ratioRightIn())

        self.__ratioRightOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "ratioRightOutButton")
        self.__ratioRightOutButton.clicked.connect(lambda:self.__ratioRightOut())

        self.__ratioLeftOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "ratioLeftOutButton")
        self.__ratioLeftOutButton.clicked.connect(lambda:self.__ratioLeftOut())

        self.__ratioLeftInButton = self.__dlg.findChild(QtWidgets.QPushButton , "ratioLeftInButton")
        self.__ratioLeftInButton.clicked.connect(lambda:self.__ratioLeftIn())

        self.__moveTopOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveTopOutButton")
        self.__moveTopOutButton.clicked.connect(lambda:self.__moveTopOut())

        self.__moveTopInButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveTopInButton")
        self.__moveTopInButton.clicked.connect(lambda:self.__moveTopIn())

        self.__moveBottomOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveBottomOutButton")
        self.__moveBottomOutButton.clicked.connect(lambda:self.__moveBottomOut())

        self.__moveBottomInButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveBottomInButton")
        self.__moveBottomInButton.clicked.connect(lambda:self.__moveBottomIn())

        self.__moveRightInButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveRightInButton")
        self.__moveRightInButton.clicked.connect(lambda:self.__moveRightIn())

        self.__moveRightOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveRightOutButton")
        self.__moveRightOutButton.clicked.connect(lambda:self.__moveRightOut())

        self.__moveLeftOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveLeftOutButton")
        self.__moveLeftOutButton.clicked.connect(lambda:self.__moveLeftOut())

        self.__moveLeftInButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveLeftInButton")
        self.__moveLeftInButton.clicked.connect(lambda:self.__moveLeftIn())
        
        self.__zoomInButton = self.__dlg.findChild(QtWidgets.QPushButton , "zoomInButton")
        self.__zoomInButton.clicked.connect(lambda:self.__zoomIn())

        self.__zoomOutButton = self.__dlg.findChild(QtWidgets.QPushButton , "zoomOutButton")
        self.__zoomOutButton.clicked.connect(lambda:self.__zoomOut())

        self.__replaceResolutionUpButton = self.__dlg.findChild(QtWidgets.QPushButton , "replaceResolutionUpButton")
        self.__replaceResolutionUpButton.clicked.connect(lambda:self.__replaceResolutionUp())

        self.__replaceResolutionDownButton = self.__dlg.findChild(QtWidgets.QPushButton , "replaceResolutionDownButton")
        self.__replaceResolutionDownButton.clicked.connect(lambda:self.__replaceResolutionDown())




     # getting parameter from first page
        self.__demLayer = firstPageClass.getDemLayer()
        self.__splitLineLayer = firstPageClass.getSplitLineLayer()
      
     # getting rasterLayer parameter
        self.__demSize = self.__getRasterSize()

     # detect if selected geometry onchange

        self.__currentSelectedGeometryID=None
        #"""
        self.__splitLineLayer.startEditing()
        self.__splitLineLayer.selectionChanged.connect(lambda:self.__reFreshPlotWidget())
        self.__splitLineLayer.geometryChanged.connect(lambda:self.__reFreshPlotWidget())
        #"""

    # dialog functions
    #-----------------------------------------------------------
  
    def __save(self):
        return 0

    def __restore(self):
        self.__reFreshPlotWidget()

    def __replace(self , resolution:float):
        try:
            features = list(self.__splitLineLayer.selectedFeatures())
            xyzList = self.__getRasterValuesXYZ(features[0].geometry() , resolution=resolution)
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
        if(self.__rasterReplaceResolution +1 <50.0):
            self.__rasterReplaceResolution  = self.__rasterReplaceResolution  +1
        else:
            self.__rasterReplaceResolution = self.__rasterDetectLength
        self.__replace(resolution=self.__rasterReplaceResolution)

    def __replaceResolutionDown(self):
        if(self.__rasterReplaceResolution -1 <self.__rasterDetectLength):
            self.__rasterReplaceResolution  = 50.0
        else:
            self.__rasterReplaceResolution = self.__rasterReplaceResolution -1
        self.__replace(resolution=self.__rasterReplaceResolution)

    #plot widget
    #------------------------------------------------------------
    def __reFreshPlotWidget(self):
        # clear plot widge
        self.__plotClass.clear()
        self.__currentSelectedGeometryID=None
        self.__rasterReplaceResolution = self.__rasterDetectLength

        # get geometry
        geometryList=[]
        selectedFeature=None
        try:
            features = list(self.__splitLineLayer.selectedFeatures())
            selectedFeature = features[0]
            for featureIndex in range(0,10):
                geometryList.append(features[featureIndex].geometry())
        except:
            print("select" + str(len(geometryList)))
        
        # start plotting

        # plot primary
        if len(geometryList)>0:
            # get geometryID
            try:
                self.__currentSelectedGeometryID = selectedFeature["id"]
            except:
                print("__reFreshPlotWidget get geometryID ")


            # plot primary line
            geometryValueList = self.__getRasterValuesYZ(geometryList[0])
            self.__plotClass.addDataPrimary(geometryValueList)

        # plot sbkCrossSection

            # add data to tableWidget and plot line
            try:
                # parse json formate to data format
                # data format : [[x1,y1],[x2,y2]....[xn,yn]]
                yzLine = json.loads(selectedFeature["profile"]) 

                # normalize the yzLine, to make centerX to 0
                # data format : [[[x1,x2...xn] , [y1,y2.....yn]]]
                yzLine = self.__plotClass.dataNormalize(yzLine)

                # add to tableWidget
                #-------------------------------------------------
                verticeList = list(list(self.__splitLineLayer.selectedFeatures())[0].geometry().vertices())
                
                # add startPoint
                startX = verticeList[0].x()
                startY = verticeList[0].y()
                startZ = 0.0
                try:
                    startZ = verticeList[0].z()
                except:
                    print("error parse startPoint")
                self.__tableClass.setStartPoint(startX , startY , startZ)

                # add endPoint
                endX = verticeList[-1].x()
                endY = verticeList[-1].y()
                endZ = 0.0
                try:
                    endZ = verticeList[-1].z()
                except:
                    print("error parse endPoint")
                self.__tableClass.setEndPoint(endX , endY , endZ)

                # add other points
                yList = yzLine[0]
                zList = yzLine[1]
                
                for index in range(0,len(yList)):
                    self.__tableClass.addPoint(yList[index] , zList[index])

                #reload table
                self.__tableClass.reload()

            except:
                traceback.print_exc()
                print("error table create faild")

                

            # set title
            try:
                 self.__plotClass.setTitle(self.__currentSelectedGeometryID)
            except:
                self.__plotClass.setTitle("no sbk selected")
                

        # plot otherLine
        if len(geometryList)>1:

            # plot line from hyDem raster
            for index in range(1,len(geometryList)):
                
                # valueList from hyDEM which from splitLine
                geometryValueList = self.__getRasterValuesYZ(geometryList[index])
                self.__plotClass.addDataSecondary(geometryValueList)

        # plot on widget
        self.__plotClass.plotPrimary()
        self.__plotClass.plotSecondary()

    # get Raster layer properties
    def __getRasterValuesYZ(self , geometry):
        temptGeometry = geometry.densifyByDistance(self.__demSize / 2.)
        temptVertices = list(temptGeometry.vertices())
        startPoint = [temptVertices[0].x() , temptVertices[0].y()]
        outputList = []

        # create vertice
        for vertice in temptVertices:
            temptX = vertice.x() - startPoint[0]
            temptY = vertice.y() - startPoint[1]
            temptDis = math.sqrt(pow(temptX , 2) + pow(temptY , 2))

            res = self.__demLayer.dataProvider().identify(QgsPointXY(vertice.x() , vertice.y()), QgsRaster.IdentifyFormatValue).results()           
            try:
                 outputList.append([temptDis , res[1]])
            except:
                pass  
        return outputList
    
    # get Raster layer properties
    def __getRasterValuesXYZ(self , geometry , resolution:float):
        temptGeometry = geometry.densifyByDistance(resolution)
        temptVertices = list(temptGeometry.vertices())
        outputList = []

        # create vertice
        for vertice in temptVertices:
            try:
                res = self.__demLayer.dataProvider().identify(QgsPointXY(vertice.x() , vertice.y()), QgsRaster.IdentifyFormatValue).results()  
                outputList.append([vertice.x() , vertice.y() , res[1]])
            except:
                outputList.append([vertice.x() , vertice.y() , 0.0])  
        return outputList

    def __getRasterSize(self):
        pixelX = self.__demLayer.rasterUnitsPerPixelX()
        pixelY = self.__demLayer.rasterUnitsPerPixelY()

        return math.sqrt(pow(pixelX , 2) + pow(pixelY , 2))