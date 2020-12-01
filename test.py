import requests
import json
from  AtCommonPython.Usual.AtFileWriter import  AtFileWriter
from multiprocessing.dummy import Pool


class test():
    def run(self):
        feature = []

        pool = Pool(10)
        feature.append(pool.apply_async(requests.get , ["https://h2-demo.pointing.tw/api/cross-sections/tainan"]))

        print(feature[0].text)



if __name__ == '__main__':
    test().run()