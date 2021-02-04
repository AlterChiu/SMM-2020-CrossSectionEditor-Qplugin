import requests
import json
from AtCommonPython.Usual.AtFileWriter import AtFileWriter
from multiprocessing.dummy import Pool


class test():
    def run(self):

        # pointJson = {
        #     "type": "LineString", "coordinates": [[189491.30734824857790954, 2534505.95786396693438292], [189440.05745175143238157, 2534286.71833603223785758]]
        # }

        pointJson = {
            "type": "point", "coordinates": [189491.30734824857790954, 2534505.95786396693438292]
        }

        header = {"content-type": "application/json"}
        request = None
        try:
            request = requests.post(
                "https://h2-demo.pointing.tw/service/dem/profile?resolution=1", data=json.dumps(pointJson), headers=header, timeout=3)
        except:
            pass
        print(request.text)


if __name__ == '__main__':
    test().run()
