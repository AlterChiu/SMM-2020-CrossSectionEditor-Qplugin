import pyqtgraph as pyqtgraph
from pyqtgraph import PlotWidget, plot
from PyQt5 import QtCore

# system py
import sys
import traceback
import statistics
import json


class PlotWidgetClass:

    # layerFeatureData
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

    def __init__(self, plotWidget: pyqtgraph.PlotWidget, layerFeatureData):
        self.__plotWidget = plotWidget
        self.__featureDatas = layerFeatureData
        self.__referentId = None

        self.__labelMaxY = 10
        self.__labelMinY = -3

        # set background in white
        self.__plotWidget.setBackground("w")

        # set grid
        self.__plotWidget.showGrid(x=True, y=True)

        # set label
        self.__labelStyle = {
            "color": "black",
            "font-weight": "bold",
            "font-size": "16px",
        }
        self.__plotWidget.setLabel('left', "Level(m)", **self.__labelStyle)
        self.__plotWidget.setLabel(
            "bottom", "Index", **self.__labelStyle)

        self.__line = {
            "leftHight": None,
            "rightHight": None,
            "bottomHight": None,
            "activeLine": None,
            "hoverLine": None
        }

    def plot(self, referentId: str):
        self.__referentId = referentId
        self.__plotWidget.setTitle(self.__referenctId)

        self.__plotHeight()
        
        self.__labelMaxY = self.__featureDatas[self.__referentId][-1]["leftHight"] +2
        self.__labelMinY = self.__featureDatas[self.__referentId][-1]["leftHight"] -2
        self.__plotWidget.setXRange(
            len(self.__featureDatas[self.__referentId])+1, -1, padding=0)
        self.__plotWidget.setYRange(
            self.__labelMaxY, self.__labelMinY, padding=0)

    # height
    # ==================================================================
    def __plotHeight(self):
        self.__clearHeight()
        color = {
            "leftHight": "k",
            "rightHight": "m",
            "bottomHight": "b"
        }

        try:
            temptXList = []
            temptLeftList = []
            temptRightList = []
            temptBottomList = []

            for profileObject in self.__featureDatas[self.__referentId]:
                temptLeftValue = None
                temptRightValue = None
                temptBottomtValue = None

                try:
                    temptLeftValue = profileObject["leftHight"]
                    temptRightValue = profileObject["rightHight"]
                    temptBottomtValue = profileObject["bottomHight"]

                except:
                    traceback.print_exc()

                if temptLeftValue != None and temptRightValue != None and temptBottomtValue != None:
                    temptXList.append(len(temptXList))
                    temptLeftList.append(temptLeftValue)
                    temptRightList.append(temptRightValue)
                    temptBottomList.append(temptBottomtValue)

            # plot Left
            self.__line["leftHight"] = self.__plotWidget.plot(
                temptXList, temptLeftValue, pen=pyqtgraph.mkPen(color=color["leftHight"]), symbol="o", symbolSize=10, symbolBrush=(color["leftHight"]))

            # plot Right
            self.__line["righttHight"] = self.__plotWidget.plot(
                temptXList, temptRightList, pen=pyqtgraph.mkPen(color=color["righttHight"]), symbol="o", symbolSize=10, symbolBrush=(color["righttHight"]))

            # plot Bottom
            self.__line["bottomHight"] = self.__plotWidget.plot(
                temptXList, temptLeftValue, pen=pyqtgraph.mkPen(color=color["bottomHight"]), symbol="o", symbolSize=10, symbolBrush=(color["bottomHight"]))

        except:
            traceback.print_exc()
            print("error while plot bankLine")

    def __clearHeight(self):
        for heightType in ["leftHight", "rightHight", "bottomHight"]:
            try:
                self.__line[heightType].clear()
                self.__line[heightType] = None
            except:
                pass

    # selection
    # ==================================================================
    def plotActive(self, index: int):
        self.__clearActive()
        self.__plotSelection(index, "activeLine")

    def __clearActive(self):
        try:
            self.__line["activeLine"].clear()
            self.__line["activeLine"] = None
        except:
            pass

    def plotHover(self, index: int):
        self.__clearActive()
        self.__plotSelection(index, "hoverLine")

    def __clearActive(self):
        try:
            self.__line["hoverLine"].clear()
            self.__line["hoverLine"] = None
        except:
            pass

        # selectedType for [activeLine , hoverLine]

    def __plotSelection(self, index: int, selectedType: str):
        color = {
            "activeLine": "r",
            "hoverLine": "y"
        }

        try:
            temptXList = []
            temptYList = []

            # left
            try:
                temptYList.append(
                    self.__featureDatas[self.__referentId][index]["leftHight"])
                temptXList.append(index)
            except:
                pass

            # right
            try:
                temptYList.append(
                    self.__featureDatas[self.__referentId][index]["rightHight"])
                temptXList.append(index)
            except:
                pass

            # bottom
            try:
                temptYList.append(
                    self.__featureDatas[self.__referentId][index]["bottomHight"])
                temptXList.append(index)
            except:
                pass

            # plot
            self.__line[selectedType] = self.__plotWidget.plot(
                temptXList, temptLeftValue, pen=pyqtgraph.mkPen(color=color["selectedType"]))

        except:
            traceback.print_exc()
            print("error while plot selection")

    # public
    #=====================================================================
    def getCrossSectionSize(self) -> int:
        try:
            return len(self.__featureDatas[self.__referentId])
        except:
            return 0