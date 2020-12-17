import requests
import json
from  AtCommonPython.Usual.AtFileWriter import  AtFileWriter
from multiprocessing.dummy import Pool


class test():
    def run(self):
        data = {"startPoint":[123,54],"endPoint":[123,88],"profile":[[0,120],[29,110]]}
        header = {"content-type":"application/json"}
        request = requests.patch("https://h2-demo.pointing.tw/api/cross-sections/tainan/X165562-Y2534976" ,data=json.dumps(data),headers=header)

        print(request.text)



if __name__ == '__main__':
    test().run()