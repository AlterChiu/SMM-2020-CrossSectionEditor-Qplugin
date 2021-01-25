import requests
import json
from  AtCommonPython.Usual.AtFileWriter import  AtFileWriter
from multiprocessing.dummy import Pool

class test():
    def run(self):
        data = { "TYPE": "point", "coordinates": [263263.173026617,2763502.7424211]}
        header = {"content-type":"application/json"}
        request = requests.post("https://h2-demo.pointing.tw/service/dem/profile?resolution=1" ,data=json.dumps(data),headers=header)


        requestJson = json.loads(request.text)
        z = requestJson["profile"][0]["z"]
        print( requestJson["profile"][0]["z"])


if __name__ == '__main__':
    test().run()