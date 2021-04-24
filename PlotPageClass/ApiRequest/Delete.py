import requests


class Delete:

    @staticmethod
    def deleteCrossSection(region, crossSectionId):

        # request
        header = {"content-type": "application/json"}

        try:
            request = requests.delete(
                "https://h2-demo.pointing.tw/api/cross-sections/" + region + "/" + crossSectionId, headers=header, timeout=3)

            if request.status_code == requests.codes.ok:
                print("delecte sussecces")
            else:
                print("delecte faild")
        except:
            print("delecte faild")
