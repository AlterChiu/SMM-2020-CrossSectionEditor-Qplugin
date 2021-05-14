
import requests
import json
from qgis.core import QgsWkbTypes, QgsPointXY, QgsRaster
import traceback

class DemLevel:
    
    # get Raster layer properties
    @staticmethod
    def getRasterValuesXYZ(geometry):

        requestPoints = DemLevel.getRasterValue(geometry)
        outList = []

        for point in requestPoints:
            outList.append([point["x"], point["y"], point["z"]])

        return outList

    # return api request profile = profile:[{x,y,dy,z}....]
    @staticmethod
    def getRasterValue(geometry) -> list:

        # get vertice from geometry
        temptVertices = list(geometry.vertices())
        startPoint = [temptVertices[0].x(), temptVertices[0].y()]
        endPoint = [temptVertices[-1].x(), temptVertices[-1].y()]

        # create api request parameters
        try:
            pointJson = {
                "type": "Lintstring", "coordinates": [startPoint, endPoint]
            }
            header = {"content-type": "application/json"}
            request = requests.post(
                "https://h2-demo.pointing.tw/service/dem33/profile?resolution=1", data=json.dumps(pointJson), headers=header, timeout=3)

            if request.status_code == requests.codes.ok:

                # request jsonObject
                return json.loads(request.text)["profile"]
            else:
                print("get dem level request faild")
                return [{"x": 0, "y": 0, "dy": 0, "z": 0}]
        except:
            # return empty json format
            traceback.print_exc()
            return [{"x": 0, "y": 0, "dy": 0, "z": 0}]
            
            


    @staticmethod
    def getPointZValue(x, y):

        pointJson = {
            "type": "point", "coordinates": [x, y]
        }
        header = {"content-type": "application/json"}

        request = None
        try:
            request = requests.post(
                "https://h2-demo.pointing.tw/service/dem/profile?resolution=1", data=json.dumps(pointJson), headers=header, timeout=3)
            requestJson = json.loads(request.text)

            if request.status_code == requests.codes.ok:
                return requestJson["profile"][0]["z"]
            else:
                return 0
        except:
            return 0 
        
    @staticmethod
    #data format : [{"x":x , "y":y , "dy" :dy ,"z":z}]
    def wrapXYZResolution(originalList:list , resolution:float=1.0):
        
        # classify request by dy(key) and z(value list)
        yzList = {}
        for point in originalList:
            multiple = (int)(point["dy"]/resolution)
            temptList = yzList.get(multiple, [])
            temptList.append(point["z"])
            yzList[multiple] = temptList

        # make yzList to output format [{x,y,dy,z}]
        outList = []

        # add startPoint
        outList.append(originalList[0])
        
        # get total length
        length = pow(pow(originalList[0]["x"] - originalList[-1]["x"], 2) +
                pow(originalList[0]["y"] - originalList[-1]["y"], 2), 0.5)
        
        # get distance
        disX = originalList[-1]["x"] - originalList[0]["x"]
        disY = originalList[-1]["y"] - originalList[0]["y"]
        
        # make classified yzList to mean value
        for key in yzList.keys():
            try:
                sumValue = sum(yzList[key])
                meanValue = sumValue/len(yzList[key])
                temptX = originalList[0]["x"] + disX*(key*resolution/length)
                temptY = originalList[0]["y"] + disY*(key*resolution/length)
                temptDY = resolution*key

                outList.append({"x": temptX, "y": temptY,
                                "dy": temptDY, "z": meanValue})
            except:
                traceback.print_exc()
                pass

        # add endPoint
        outList.append(originalList[-1])

        return outList
