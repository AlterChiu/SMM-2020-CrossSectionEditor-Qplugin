from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication,QPushButton,QLabel,QComboBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsWkbTypes,QgsProcessingUtils,QgsVectorLayer,QgsProject,QgsCoordinateReferenceSystem
from AtCommonPython.Qgis.AtQgis import AtQgisGui
from AtCommonPython.Deltares.Sobek.SobekFileReader import SobekFileReader
from AtCommonPython.Usual.AtFileWriter import AtFileWriter
from ..FramePage import PlotPage
from ..PlotPageClass.PlotPageClass import PlotPageClass
import requests
import traceback
import json

import sys
import os

class FirstPageClass:
    def __init__(self , currentDlg):
        self.__dlg = currentDlg
        self.__demComboBox = currentDlg.findChild(QtWidgets.QComboBox , "DemComboBox")
        self.__countyComboBox = currentDlg.findChild(QtWidgets.QComboBox , "CountyComboBox")

        self.__nextButton = currentDlg.findChild(QtWidgets.QPushButton , "NextButton")


        # initial comboBox
        self.__initialDemComboBox()
        self.__initialCountyComboBox()

        # setting connection
        self.__demComboBox.activated.connect(lambda:self.__initialDemComboBox())
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
    def __initialDemComboBox(self):
        self.__demComboBox.clear()
        for layer in AtQgisGui().getRasterLayer():
            self.__demComboBox.addItem(layer.name() , layer)

    # CountyComboBox
    #----------------------------------------------------------------------------
    def __initialCountyComboBox(self):
        self.__countyComboBox.clear()
        try:
            request = requests.get("https://h2-demo.pointing.tw/api/cross-sections/")
            for county in request.json():
                countyName = str(county["name"])
                self.__countyComboBox.addItem(countyName , str(county["id"]))
        except:
            traceback.print_exc()
            self.__countyComboBox.addItem("連結伺服器失敗")

    # NextButtonGui
    #----------------------------------------------------------------------------
    def __toNextPage(self):
      
      #check every input layer is exist
      #----------------------------------------------------------------------
        checker = 0
        self.__nextButton.setEnabled(False)

      # ckeckDem
        if self.__demComboBox.currentText == "":
            Exception("splitLine could not be null")
            checker = 1
            self.__nextButton.setEnabled(True)

      # turn to next page
        if checker == 0:
            
            # get crossSection json file
            crossSectionTemptPath = QgsProcessingUtils.tempFolder() + str("\\crossSection.json")
            try:
                # save crossSection json to file
                # request = requests.get("https://h2-demo.pointing.tw/api/cross-sections/" + self.__countyComboBox.currentData())
                # temptJson = json.loads(request.text)
                
                
                # test
                temptJson = None
                temptPaht = os.path.dirname(__file__)
                with open(temptPaht + "/testCrossSection.json") as temptText:
                    temptJson = json.load(temptText)
                
                self.__editCounty = self.__countyComboBox.currentData()

                # make the geometry only has start and endPoint in it
                for feature in temptJson["features"]:
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
                    
                # write json to temptFile
                writer = AtFileWriter(json.dumps(temptJson), crossSectionTemptPath).textWriter("")

                # load tempt jsonFile as layer
                self.__splitLineLayer = QgsVectorLayer(crossSectionTemptPath,"crossSection" , "ogr")
                self.__splitLineLayer.setCrs(QgsCoordinateReferenceSystem(3826),True)
                QgsProject.instance().addMapLayer(self.__splitLineLayer)

            except:
                traceback.print_exc()

            # setting output paramter
            self.__demLayer = self.__demComboBox.currentData()

            # disconnect
            self.__nextButton.disconnect()
            self.__demComboBox.disconnect()

            # close dlg and open another
            self.__dlg.done(0)
            self.__isClose = True
            self.__dlg = PlotPage()
            self.__dlg.show()

            # create plotPageClass
            PlotPageClass(self.__dlg , self)

        