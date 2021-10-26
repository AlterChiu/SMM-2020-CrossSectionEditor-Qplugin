from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication,QPushButton,QLabel,QComboBox,QFileDialog
from qgis.gui import QgsFileWidget
from qgis.core import QgsWkbTypes,QgsProcessingUtils,QgsVectorLayer,QgsProject,QgsCoordinateReferenceSystem,QgsMapLayer
from AtCommonPython.Qgis.AtQgis import AtQgisGui
from AtCommonPython.Deltares.Sobek.SobekFileReader import SobekFileReader
from AtCommonPython.Usual.AtFileWriter import AtFileWriter
from ..FramePage import PlotPage
from ..PlotPageClass.PlotPageClass import PlotPageClass
import requests
import traceback
import json
import gdal
import pathlib

import sys
import os

class FirstPageClass:
    def __init__(self , currentDlg):
        self.__dlg = currentDlg
        self.__apiComboBox = currentDlg.findChild(QtWidgets.QComboBox , "ApiComboBox")
        self.__countyComboBox = currentDlg.findChild(QtWidgets.QComboBox , "CountyComboBox")
        self.__crossectionComboBox = currentDlg.findChild(QtWidgets.QComboBox , "CrossSectionComboBox")
        self.__demComboBox = currentDlg.findChild(QtWidgets.QComboBox , "DEMComboBox")

        self.__SelectLocalFile = currentDlg.checkBox.isChecked()
        self.__nextButton = currentDlg.findChild(QtWidgets.QPushButton , "NextButton")
        
        # set local file select False
        self.__crossectionComboBox.setEnabled(False)
        self.__demComboBox.setEnabled(False)

        # setting check box connection
        self.__dlg.checkBox.stateChanged.connect(self.changefunction)
        # initial comboBox
        self.__initialApiComboBox(True)
        # setting connection
        self.__apiComboBox.activated.connect(lambda:self.__initialApiComboBox(False))
        self.__nextButton.clicked.connect(lambda:self.__toNextPage())

        # output parameter
        self.__splitLineLayer = None
        self.__demLayer = None

        # edit county
        self.__editCounty = None

        # check isClosed
        self.__isClose = False


    # output function
    #----------------------------------------------------------------------------
    def getSplitLineLayer(self):
        return self.__splitLineLayer

    def getEditorCounty(self):
        return self.__editCounty


    def getDemLayer(self):
        return self.__demLayer

    def isClosed(self):
        return self.__isClose

    # demGui
    #----------------------------------------------------------------------------
    def __initialApiComboBox(self,first:bool):
        if first:
            self.__apiComboBox.clear()
            ApiList =  {
                        'h2-demo.pointing.tw':'https://h2-demo.pointing.tw/api/cross-sections/',
                        '192.168.50.78:8080':'http://192.168.50.78:8080/api/cross-sections/',
                        'test.pointing.tw':'http://test.pointing.tw/h2/api/cross-sections/',
                        }
            for key,prop in ApiList.items():
                self.__apiComboBox.addItem(key , prop)

        self.__initialCountyComboBox(self.__apiComboBox.currentData())


    # CountyComboBox
    #----------------------------------------------------------------------------
    def __initialCountyComboBox(self,api):
        self.__countyComboBox.clear()
        try:
            request = requests.get(api)
            

            for county in request.json():
                countyName = str(county["basinName"])
                self.__countyComboBox.addItem(countyName , str(county["basinId"]))
        except:
            traceback.print_exc()
            self.__countyComboBox.addItem("連結伺服器失敗")


    # select local file function
    #----------------------------------------------------------------------------
    def changefunction(self):
        if self.__SelectLocalFile:
            self.__apiComboBox.setEnabled(True)
            self.__countyComboBox.setEnabled(True)
            self.__crossectionComboBox.setEnabled(False)
            self.__demComboBox.setEnabled(False)
            self.__crossectionComboBox.clear()
            self.__demComboBox.clear()
            self.__SelectLocalFile = False
        else:
            self.__apiComboBox.setEnabled(False)
            self.__countyComboBox.setEnabled(False)
            self.__crossectionComboBox.setEnabled(True)
            self.__demComboBox.setEnabled(True)
            lyr = [layer for layer in QgsProject.instance().mapLayers().values()]
            for layer in lyr:
                if layer.type() == QgsMapLayer.VectorLayer:
                    self.__crossectionComboBox.addItems([layer.name()])
                elif layer.type() == QgsMapLayer.RasterLayer:
                    self.__demComboBox.addItems([layer.name()])
            self.__SelectLocalFile = True


    # NextButtonGui
    #----------------------------------------------------------------------------
    def __toNextPage(self):
      #check every input layer is exist
      #----------------------------------------------------------------------
        checker = 0
        self.__nextButton.setEnabled(False)

      # ckeckDem
        if True:
            Exception("splitLine could not be null")
            checker = 0
            self.__nextButton.setEnabled(True)

      # turn to next page
        if checker == 0:
            if self.__SelectLocalFile:
                # get crossSection json file
                crossSectionTemptPath = QgsProcessingUtils.tempFolder() + str("\\crossSection.json")
                try:
                    # save crossSection json to file
                    #temptJson = json.loads(self.__crossection)
                    layer = QgsProject.instance().mapLayersByName(self.__crossectionComboBox.currentText())[0]
                    layer_path = str(layer.source()).split("|")[0]
                    f = open(layer_path,encoding="utf-8")
                    temptJson = json.load(f)
                    temptPath = os.path.dirname(__file__)
                    # test
                    '''
                    temptJson = None
                    temptPath = os.path.dirname(__file__)
                    with open(temptPath + "/testCrossSection.json") as temptText:
                        temptJson = json.load(temptText)
                    '''
                    self.__editCounty = self.__demComboBox.currentData()

                    # make the geometry only has start and endPoint in it
                    for feature in temptJson["features"]:
                        try:
                            temptGeometryPoints = feature["geometry"]["coordinates"]
                            # outList, add a buffer to start-end point (each side for 3m)
                            outGeometryPoints =[]
                            startPoint = temptGeometryPoints[0]
                            endPoint = temptGeometryPoints[-1]
                            geometryLength = pow(pow(startPoint[0] - endPoint[0] ,2) + pow(startPoint[1] - endPoint[1] ,2),0.5)

                            startDirection = [(startPoint[0]-endPoint[0])*(3.0/geometryLength) , (startPoint[1]-endPoint[1])*(3.0/geometryLength)]
                            endDirection = [startDirection[0]*-1 , startDirection[1]*-1]

                            outGeometryPoints.append([startPoint[0]+startDirection[0] , startPoint[1]+startDirection[1]])
                            outGeometryPoints.append([endPoint[0]+endDirection[0] , endPoint[1]+endDirection[1]])
                            feature["geometry"]["coordinates"] = outGeometryPoints

                            # remove not necessary feild
                            try:
                                del feature["properties"]["originalId"]
                            except:
                                pass
                            try:
                                del feature["properties"]["node_py"]
                            except:
                                pass
                            try:
                                del feature["properties"]["node_px"]
                            except:
                                pass
                            try:
                                del feature["properties"]["node_nm"]
                            except:
                                pass
                        except:pass
                        
                    # write json to temptFile
                    writer = AtFileWriter(json.dumps(temptJson), crossSectionTemptPath).textWriter("")

                    # load tempt jsonFile as layer
                    self.__splitLineLayer = QgsVectorLayer(crossSectionTemptPath,"crossSection" , "ogr")
                    self.__splitLineLayer.setCrs(QgsCoordinateReferenceSystem(3826),True)
                    self.__splitLineLayer.loadNamedStyle(temptPath + '/style/crossSectionStyle.qml')
                    QgsProject.instance().addMapLayer(self.__splitLineLayer)

                except:
                    traceback.print_exc()
            else:
                # get crossSection json file
                crossSectionTemptPath = QgsProcessingUtils.tempFolder() + str("\\crossSection.json")
                try:
                    # save crossSection json to file
                    request = requests.get(self.__apiComboBox.currentData() + self.__countyComboBox.currentData())
                    temptJson = json.loads(request.text)
                    temptPath = os.path.dirname(__file__)
                    print(request)
                    # test
                    '''
                    temptJson = None
                    temptPath = os.path.dirname(__file__)
                    with open(temptPath + "/testCrossSection.json") as temptText:
                        temptJson = json.load(temptText)
                    '''
                    self.__editCounty = self.__countyComboBox.currentData()

                    # make the geometry only has start and endPoint in it
                    for feature in temptJson["features"]:
                        try:
                            temptGeometryPoints = feature["geometry"]["coordinates"]
                            # outList, add a buffer to start-end point (each side for 3m)
                            outGeometryPoints =[]
                            startPoint = temptGeometryPoints[0]
                            endPoint = temptGeometryPoints[-1]
                            geometryLength = pow(pow(startPoint[0] - endPoint[0] ,2) + pow(startPoint[1] - endPoint[1] ,2),0.5)

                            startDirection = [(startPoint[0]-endPoint[0])*(3.0/geometryLength) , (startPoint[1]-endPoint[1])*(3.0/geometryLength)]
                            endDirection = [startDirection[0]*-1 , startDirection[1]*-1]

                            outGeometryPoints.append([startPoint[0]+startDirection[0] , startPoint[1]+startDirection[1]])
                            outGeometryPoints.append([endPoint[0]+endDirection[0] , endPoint[1]+endDirection[1]])
                            feature["geometry"]["coordinates"] = outGeometryPoints

                            # remove not necessary feild
                            try:
                                del feature["properties"]["originalId"]
                            except:
                                pass
                            try:
                                del feature["properties"]["node_py"]
                            except:
                                pass
                            try:
                                del feature["properties"]["node_px"]
                            except:
                                pass
                            try:
                                del feature["properties"]["node_nm"]
                            except:
                                pass
                        except:pass
                        
                    # write json to temptFile
                    writer = AtFileWriter(json.dumps(temptJson), crossSectionTemptPath).textWriter("")

                    # load tempt jsonFile as layer
                    self.__splitLineLayer = QgsVectorLayer(crossSectionTemptPath,"crossSection" , "ogr")
                    self.__splitLineLayer.setCrs(QgsCoordinateReferenceSystem(3826),True)
                    self.__splitLineLayer.loadNamedStyle(temptPath + '/style/crossSectionStyle.qml')
                    QgsProject.instance().addMapLayer(self.__splitLineLayer)

                except:
                    traceback.print_exc()

            # setting output paramter
            #self.__demLayer = self.__demComboBox.currentData()

            # disconnect
            self.__nextButton.disconnect()
            #self.__demComboBox.disconnect()

            # close dlg and open another
            self.__dlg.done(0)
            self.__isClose = True
            self.__dlg = PlotPage()
            self.__dlg.show()

            # create plotPageClass
            PlotPageClass(self.__dlg , self)
       