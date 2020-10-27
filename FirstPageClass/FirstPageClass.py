from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication,QPushButton,QLabel,QComboBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsWkbTypes
from AtCommonPython.Qgis.AtQgis import AtQgisGui
from AtCommonPython.Deltares.Sobek.SobekFileReader import SobekFileReader
from ..FramePage import PlotPage
from ..PlotPageClass.PlotPageClass import PlotPageClass

import sys

class FirstPageClass:
    def __init__(self , currentDlg):
        self.__dlg = currentDlg
        self.__demComboBox = currentDlg.findChild(QtWidgets.QComboBox , "DemComboBox")
        self.__demAlter = currentDlg.findChild(QtWidgets.QLabel , "DemAlter")
        self.__demAlter.setStyleSheet('color:red')

        self.__splitLineComboBox = currentDlg.findChild(QtWidgets.QComboBox , "SplitLineComboBox")
        self.__splitLineFeatureComboBox = currentDlg.findChild(QtWidgets.QComboBox , "SplitLineFeatureComboBox")
        self.__splitLineAlter = currentDlg.findChild(QtWidgets.QLabel , "SplitLineAlert")
        self.__splitLineAlter.setStyleSheet('color:red')

        self.__sbkFileSelection = currentDlg.findChild(QgsFileWidget , "SbkFileSelection")
        self.__sbkAlert = currentDlg.findChild(QtWidgets.QLabel , "SbkAlert")
        self.__sbkAlert.setStyleSheet('color:red')
        
        self.__nextButton = currentDlg.findChild(QtWidgets.QPushButton , "NextButton")


        # initial comboBox
        self.__initialDemComboBox()
        self.__initialSplitLineComboBox()

        # setting connection
        self.__splitLineComboBox.activated.connect(lambda:self.__checkSplitLineComboBox(self.__splitLineComboBox.currentIndex()))
        self.__demComboBox.activated.connect(lambda:self.__initialDemComboBox())    
        self.__nextButton.clicked.connect(lambda:self.__toNextPage())

        # output parameter
        self.__splitLineLayer = None
        self.__splitLineIdTitle = None
        self.__demLayer = None
        self.__sbkProfileDictionary = {}

        # check isClosed
        self.__isClose = False

    # output function
    #----------------------------------------------------------------------------
    def getSplitLineLayer(self):
        return self.__splitLineLayer

    def getSplitLineIdFeildName(self):
        return self.__splitLineIdTitle

    def getDemLayer(self):
        return self.__demLayer

    def getSbkCrossSectionProfile(self):
        return self.__sbkProfileDictionary

    def isClosed(self):
        return self.__isClose

    # demGui
    #----------------------------------------------------------------------------
    def __initialDemComboBox(self):
        self.__demComboBox.clear()
        for layer in AtQgisGui().getRasterLayer():
            self.__demComboBox.addItem(layer.name() , layer)
    
    def __checkDemComboBox(self , selectIndex):
        selectLayer = self.__demComboBox.itemData(selectIndex)
        self.__demAlter.setText(selectLayer.name())

    # SplitLineGui
    #----------------------------------------------------------------------------
    def __initialSplitLineComboBox(self):
        self.__splitLineComboBox.clear()
        for layer in AtQgisGui().getVectorLayer():
            self.__splitLineComboBox.addItem(layer.name() , layer)
        
    def __checkSplitLineComboBox(self , selectIndex):
        selectLayer = self.__splitLineComboBox.itemData(selectIndex)
        layerFields = AtQgisGui().getAttributeTable(selectLayer)

        self.__splitLineFeatureComboBox.clear()
        for key in layerFields:
            self.__splitLineFeatureComboBox.addItem(key)

    # SbkFileReader
    #----------------------------------------------------------------------------
    def __getSbkCrossSectionProfile(self , sbkFilePath):
        outputDictionary = {}
        profileTagList = SobekFileReader(sbkFilePath).getTag("CRDS")

        for profileTagContent in profileTagList:
            tableValueList = SobekFileReader.getTag(profileTagContent , "TABLE")
            plotXY = []

            # get sobekCrossSection profile
            for index in range(1 , len(tableValueList)-1 , 3):
                plotXY.append([tableValueList[index] , tableValueList[index+1]])

            # get sobekCrossSection id
            id = str(profileTagContent[2]).replace("'" , "")

            outputDictionary[id] = plotXY
        return outputDictionary


    # NextButtonGui
    #----------------------------------------------------------------------------
    def __toNextPage(self):
      
      #check every input layer is exist
      #----------------------------------------------------------------------
        checker = 0
      
      # ckeckDem
        if self.__demComboBox.currentText == "":
            checker = 1
            self.__demAlter.setText("Dem couldn't be null")
      
      # check splitLine
        splitLineLayer = self.__splitLineComboBox.currentData()
        temptFeature = list(splitLineLayer.getFeatures())[0]
        if temptFeature.geometry().type() != QgsWkbTypes.LineGeometry:
            self.__splitLineAlter.setText("SplitLine should be a polyLine layer")
            checker = 1
        
        elif self.__splitLineFeatureComboBox.currentText() == "":
            self.__splitLineAlter.setText("SplitLine ID couldn't be null")
            checker = 1

    
      # turn to next page
        if checker == 0:
            
            # detect sbk file
            try:
                sbkFileAdd = self.__sbkFileSelection.filePath()
                self.__sbkProfileDictionary = self.__getSbkCrossSectionProfile(sbkFileAdd)
            except:
                print("open sbkFile failed\n")

            # setting output paramter
            self.__demLayer = self.__demComboBox.currentData()
            self.__splitLineLayer = self.__splitLineComboBox.currentData()
            self.__splitLineIdTitle = self.__splitLineFeatureComboBox.currentText()

            # close dlg and open another
            self.__dlg.done(0)
            self.__isClose = True
            self.__dlg = PlotPage()
            self.__dlg.show()

            # create plotPageClass
            PlotPageClass(self.__dlg , self)