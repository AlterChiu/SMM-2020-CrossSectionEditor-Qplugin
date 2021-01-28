import requests
import json
from AtCommonPython.Usual.AtFileWriter import AtFileWriter
from multiprocessing.dummy import Pool


class test():
    def run(self):
        pointJson = {
            "type": "point", "coordinates": [10, 14]
        }
        header = {"content-type": "application/json"}
        request = None
        try:
            request = requests.post(
                "https://h2-demo.pointing.tw/service/dem/profile?resolution=1", data=json.dumps(pointJson), headers=header, timeout=3)
        except:
            pass
        print(request.status_code)


if __name__ == '__main__':
    test().run()
