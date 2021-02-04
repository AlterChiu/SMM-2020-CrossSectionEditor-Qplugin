import requests
from .DemLevel import DemLevel


class Update:

    @staticmethod
    def crossSection(object):

        # {
        #     id : crossSectionID,

        #     tableDate : unChecked crossSection profile,

        #     startPoint : the left fixPoint,

        #     endPoint : the right fixPoint,

        #     leftFixPoint : leftFixPoint in [y,z]

        #     rightFixPoint : rightFixPoint in [y,z]

        # }

        try:

            # get selected feature ID
            featureID = object["id"]

            # get table data
            tableDate = object["tableDate"]

            # get fixPoints
            leftFixPoint = object["leftFixPoint"]  # [y,z]
            rightFixPoint = object["rightFixPoint"]  # [y,z]

            # get startPoint, [x,y,z]
            startPoint = object["startPoint"]
            startPoint[2] = DemLevel.getPointZValue(
                startPoint[0], startPoint[1])

            # get endPoint, [x,y,z]
            endPoint = object["startPoint"]
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
                if rowData[2] > float(leftFixPoint[0]) and rowData[2] < float(rightFixPoint[0]):
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
