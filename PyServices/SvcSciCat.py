from __future__ import print_function

import Daisy
import requests
import json
class SvcSciCat(Daisy.Base.DaisySvc):

    class GenerateDataset:
        def __init__(self, pidprefix='CSTR:17081.11bsrf.3w1.'):
            self.__datafile_list = []
            self.__datafile_size = 0
            self.__worker_name   = 'Daisy'
            self.__pid = pidprefix

        def __getCheckSum(self, filename):
            from hashlib import md5
            with open(filename, 'rb') as f:
                s = md5(f.read()).hexdigest()
                return s

        def addFile(self, filename=''):
            import os
            if os.path.exists(filename) == False:
                return False
            filename = os.path.abspath(filename)
            filesize = os.path.getsize(filename)
            filetime = os.path.getmtime(filename)
            fileuid  = os.stat(filename).st_uid
            filegid  = os.stat(filename).st_gid
            fileperm = oct(os.stat(filename).st_mode)[-3:]
            filechk  = self.__getCheckSum(filename)
            self.__datafile_list.append({
                     'path':filename,
                     'size':filesize,
                     'time':filetime,
                     'chk' :filechk,
                     'uid' :fileuid,
                     'gid' :filegid,
                     'perm':fileperm})
            if self.__datafile_size == 0:
                import uuid
                self.__pid = self.__pid + str(uuid.uuid4())   

            if (self.__datafile_size + 1) == len(self.__datafile_list):
                self.__datafile_size = self.__datafile_size + 1
            else:
                print('Warning: update file')
                self.__datafile_size = len(self.__datafile_list)

        def getPID(self):
            return self.__pid

        def getJSON(self):
            ret_JSON = json.dumps({
                     'size':self.__datafile_size,
                     'dataFileList':self.__datafile_list,
                     'updateBy':self.__worker_name})
            return ret_JSON

    def __init__(self, name):
        super().__init__(name)
        self.headers      = {"Content-Type": "application/json;charset=UTF-8"}
        self.__generateDataset = self.GenerateDataset()
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

    def setDataset(self):
        data_json = self.__generateDataset.getJSON()
        pid = self.__generateDataset.getPID()
        url = self.access_point+'OrigDatablocks/upsertWithWhere?where={"datasetId":"'+pid+'"}&access_token='+self.__login()
        print(url)
        print(data_json)
        r = requests.post(url=url,json=data_json,headers=self.headers)

    def updateDataset(self, filename):
        self.__generateDataset.addFile(filename) 

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






