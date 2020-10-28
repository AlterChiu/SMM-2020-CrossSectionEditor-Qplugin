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

#userCreate py
from .PlotWidgetClass import PlotWidgetClass
from .TableWidgeClass import TableWidgeClass


class PlotPageClass:
    def __init__(self , dlg, firstPageClass):

     # constant
        self.__rasterDetectLength = 0.5
    
     # get dlg
        self.__dlg = dlg

     # get object in plot page
        
        # plot widget
        self.__plotWidget = self.__dlg.findChild(pyqtgraph.PlotWidget , "plotWidget")
        self.__plotClass = PlotWidgetClass(self.__plotWidget)

        # table widget
        self.__editTable = self.__dlg.findChild(QtWidgets.QTableWidget , "editTableWidget")
        self.__tableClass = TableWidgeClass(self.__editTable)


        self.__saveButton = self.__dlg.findChild(QtWidgets.QPushButton , "SaveButton")
        self.__restoreButton = self.__dlg.findChild(QtWidgets.QPushButton , "RestoreButton")
        self.__reverseButton = self.__dlg.findChild(QtWidgets.QPushButton , "ReverseButton")

        self.__moveUpButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveUp")
        self.__moveDownButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveDown")
        self.__moveRightButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveRight")
        self.__moveLeftButton = self.__dlg.findChild(QtWidgets.QPushButton , "moveLeft")

     # getting parameter from first page
        self.__demLayer = firstPageClass.getDemLayer()
        self.__splitLineLayer = firstPageClass.getSplitLineLayer()
        self.__splitLineIdFeildName = firstPageClass.getSplitLineIdFeildName()
        self.__sbkCrossSectionProfile = firstPageClass.getSbkCrossSectionProfile()
      
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
    def __initialTable(self):
        return 0
  
    def __saveSplitLineVectorLayer(self):
        self.__splitLineLayer.commitChanges()


    #plot widget
    #------------------------------------------------------------
    def __reFreshPlotWidget(self):
        # clear plot widge
        self.__plotClass.clear()
        self.__currentSelectedGeometryID=None

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
            geometryValueList = self.__getRasterValues(geometryList[0])
            self.__plotClass.addDataPrimary(geometryValueList)

        # plot sbkCrossSection

            # add data to tableWidget and plot line
            try:
                # parse json formate to data format
                # data format : [[x1,y1],[x2,y2]....[xn,yn]]
                yzLine = json.loads(selectedFeature["profile"]) 

                # normalize the yzLine, to make centerX to 0
                # data format : [[[x1,x2...xn] , [y1,y2.....yn]]]
                yzLine = self.__plotClass.addDataSBK(yzLine)

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
                yList = yzLine[0][0]
                zList = yzLine[0][1]
                
                for index in range(0,len(yList)):
                    self.__tableClass.addPoint(yList[index] , zList[index])

            except:
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
                geometryValueList = self.__getRasterValues(geometryList[index])
                self.__plotClass.addDataSecondary(geometryValueList)

        # plot on widget
        self.__plotClass.plot()

    # get Raster layer properties
    def __getRasterValues(self , geometry):
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
        
    def __getRasterSize(self):
        pixelX = self.__demLayer.rasterUnitsPerPixelX()
        pixelY = self.__demLayer.rasterUnitsPerPixelY()

        return math.sqrt(pow(pixelX , 2) + pow(pixelY , 2))