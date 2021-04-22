class Create:

    @staticmethod
    def createCrossSection(startPoint: list, endPoint: list, profile: list, region) -> str:

        # create request body
        requestBody = {}
        requestBody["startPoint"] = startPoint
        requestBody["endPoint"] = endPoint
        requestBody["profile"] = profile
        requestBody["referencePoint"] = [
            (startPoint[0] + endPoint[0])/2, (startPoint[1] + endPoint[1])/2]

        # request
        header = {"content-type": "application/json"}

        try:
            request = requests.post(
                "https://h2-demo.pointing.tw/api/cross-sections/" + region, data=json.dumps(requestBody), headers=header, timeout=3)
            
            return "testCrossSection"
        except:
            return "testCrossSection"       