import requests
import json
from AtCommonPython.Usual.AtFileWriter import AtFileWriter
from multiprocessing.dummy import Pool


class test():
    def run(self):

        data = [{"key":1, "value":1}, {"key":2, "value":2}, {"key":3, "value":3}]
        
        print(min(data , key = lambda x : x["value"])["key"])


if __name__ == '__main__':
    test().run()
