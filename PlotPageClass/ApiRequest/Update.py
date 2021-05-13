import requests
import math
import traceback
import json
from .DemLevel import DemLevel


class Update:
    
    @staticmethod
    def crossSection(object , selectedFeature , selectedLayer):

        # {
        #     id : crossSectionID,

        #     tableData : unChecked crossSection profile,

        #     startPoint : the left fixPoint,

        #     endPoint : the right fixPoint,

        #     leftFixPoint : leftFixPoint in [y,z]

        #     rightFixPoint : rightFixPoint in [y,z]

        # }
        print(object)
        try:

            # get selected feature ID
            featureID = object["id"]

            # get table data
            tableData = object["tableData"]

            # get fixPoints
            leftFixPoint = object["leftFixPoint"]  # [y,z]
            rightFixPoint = object["rightFixPoint"]  # [y,z]

            # get startPoint, [x,y,z]
            startPoint = object["startPoint"]
            startPoint[2] = DemLevel.getPointZValue(
                startPoint[0], startPoint[1])

            # get endPoint, [x,y,z]
            endPoint = object["endPoint"]
            endPoint[2] = DemLevel.getPointZValue(endPoint[0], endPoint[1])

            # get boundary length
            maxLength = math.sqrt(
                pow(startPoint[0] - endPoint[0], 2) + pow(startPoint[1] - endPoint[1], 2))

            # create output profile
            outProfile = []

            # add left fix(boundary) point
            outProfile.append(leftFixPoint)

            # add other points which within the boundary
            for rowData in tableData:  # [x,y,l,z]
                print(leftFixPoint[0])
                if rowData[2] > float(leftFixPoint[0]) and rowData[2] < float(rightFixPoint[0]):
                    outProfile.append([rowData[2], rowData[3]])

            # add end point
            outProfile.append(rightFixPoint)
            referencepoint = [(startPoint[0] + endPoint[0])/2,(startPoint[1] + endPoint[1])/2]

            # update to rest-api (patch)
            data = {"startPoint": startPoint,
                    "endPoint": endPoint, "profile": outProfile,
                    "referencePoint": referencepoint}
            header = {"content-type": "application/json"}
            request = requests.patch("http://192.168.50.78:8080/api/cross-sections/" +
                                     object["countyId"] + "/" + featureID, data=json.dumps(data), headers=header)
            print("crossSection: " + str(json.dumps(data)))

            # new id
            newID = "X" + str(int((startPoint[0] + endPoint[0])/2)) + \
                "-Y" + str(int((startPoint[1] + endPoint[1])/2))

            # commit to layer
            selectedFeature["id"] = newID
            selectedFeature["profile"] = str(outProfile)
            selectedLayer.updateFeature(selectedFeature)

        except:
            traceback.print_exc()
            Exception("save error")
