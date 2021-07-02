from __future__ import print_function

import Daisy
import requests
import json
class SvcSciCat(Daisy.Base.DaisySvc):

    def __init__(self, name):
        super().__init__(name)
        self.headers      = {"Content-Type": "application/json;charset=UTF-8"}
        pass

    def initialize(self, access_url='', username='admin', password='ihep123'):
        self.access_point = 'http://192.168.14.92:3000/api/v3/'
        self.user_info    = {"username":username, "password":password}
        self.LogInfo("initialized SvcSciCat")
        return True

    def __login(self):
        url = self.access_point+"Users/login"
        r = requests.post(url=url, json=self.user_info, headers=self.headers)
        token = (r.json()["id"])
        return (token)

    def login(self):
        return self.__login()

    def __polishPID(self, pid = None):
        if type(pid) is str:
            return pid.replace('/','%2F')
        else:
            return pid

    class generateDataset:
        import os
        from hashlib import md5
        def __init__(self):
            self.__datafile_list = []
            self.__datafile_size = NULL
            self.__worker_name   = 'Daisy'

        def getCheckSum(filename):
            with open(filename, 'rb') as f:
                s = md5.new(f.read()).hexdigest()
                return s

        def addFile(self, filename=''):
            if os.path.exists(filename) == False:
                return False
            filename = os.path.abspath(filename)
            filesize = os.path.getsize(filename)
            fileperm = oct(os.stat(filename).st_mode)[-3:]
            filechk  = self.getCheckSum(filename)


    def getDatasetInfo(self, pid = None):
        pid=self.__polishPID(pid)  
        url = self.access_point+'Datasets/'+pid+'?access_token='+self.__login()
        self.LogInfo(url)
        r=requests.get(url=url,json=self.user_info,headers=self.headers)
        return (r.json())
  
    def getPID(self, beamtimeId, scanId):
        url = self.access_point+'Datasets/findOne?filter={"where":{"scanId":"'+scanId+'","beamtimeId":"'+beamtimeId+'"}}&access_token='+self.__login()
        self.LogInfo(url)
        r=requests.get(url=url,json=self.user_info,headers=self.headers)
        pid = r.json()['pid']
        return pid

    def getDataFileList(self, pid = None):
        pid=self.__polishPID(pid)  
        url = self.access_point+'OrigDatablocks/findOne?filter={"where":{"datasetId":"'+pid+'"}}&access_token='+self.__login()
        self.LogInfo(url)
        r=requests.get(url=url,json=self.user_info,headers=self.headers)
        
        return  tuple(eachfile['path'] for eachfile in r.json()['dataFileList'])

    def execute(self):
        self.LogInfo("execute SvcSciCat, Hello Daisy ")
        return True

    def finalize(self):
        self.LogInfo("finalize SvcSciCat, Hello Daisy ")
        return True






