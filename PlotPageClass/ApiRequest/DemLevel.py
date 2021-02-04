
import requests
import json
from qgis.core import QgsWkbTypes, QgsPointXY, QgsRaster
import traceback

class DemLevel:
    
    @staticmethod
        # get Raster layer properties
    def getRasterValuesYZ(geometry, resolution: float) -> list:

        requestPoints = DemLevel.getRasterValue(geometry, resolution)
        outList = []

        for point in requestPoints:
            outList.append([point["dy"], point["z"]])

        return outList

    # get Raster layer properties
    @staticmethod
    def getRasterValuesXYZ(geometry, resolution: float):

        requestPoints = DemLevel.getRasterValue(geometry, resolution)
        outList = []

        for point in requestPoints:
            outList.append([point["x"], point["y"], point["z"]])

        return outList

    # return api request profile = profile:[{x,y,dy,z}....]
    @staticmethod
    def getRasterValue(geometry, resolution: float) -> list:

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
                "https://h2-demo.pointing.tw/service/dem/profile?resolution=1", data=json.dumps(pointJson), headers=header, timeout=3)

            if request.status_code == requests.codes.ok:

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
                    except:
                        traceback.print_exc()
                        pass

                # add endPoint
                outList.append(requestJson["profile"][-1])

                return outList
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