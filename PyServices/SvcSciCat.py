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
                self.__pid = self.__pid + str(uuid.uuid4()).replace('-','')
                print(self.__pid)

            if (self.__datafile_size + 1) == len(self.__datafile_list):
                self.__datafile_size = self.__datafile_size + 1
            else:
                print('Warning: update file')
                self.__datafile_size = len(self.__datafile_list)

        def getPID(self):
            return self.__pid

        def getDerivedDatasetJSON(self, beamtimeId, scanId, rawPID):
            ret_JSON = json.dumps({
                           "investigator": "string",
                           "inputDatasets": [
                             rawPID
                           ],
                           "usedSoftware": [
                             "string"
                           ],
                           "jobParameters": {},
                           "jobLogData": "string",
                           "scientificMetadata": {},
                           "pid": self.__pid,
                           "beamtimeId": beamtimeId,
                           "scanId": scanId,
                           "owner": "string",
                           "ownerEmail": "string",
                           "orcidOfOwner": "string",
                           "contactEmail": "string",
                           "sourceFolder": "string",
                           "size":self.__datafile_size,
                           "packedSize": 0,
                           "creationTime": "2021-07-12T02:22:45.813Z",
                           "type": "string",
                           "validationStatus": "unvalidated",
                           "keywords": [
                             "string"
                           ],
                           "description": "string",
                           "datasetName": "string",
                           "classification": "string",
                           "license": "string",
                           "version": "string",
                           "ownerGroup": "string",
                           "accessGroups": [
                             "string"
                           ],
                           "createdBy": "string",
                           "updatedBy": "string",
                           "createdAt": "2021-07-12T02:22:45.813Z",
                           "updatedAt": "2021-07-12T02:22:45.813Z",
                          })
            return ret_JSON


        def getOrigDatablocksJSON(self):

            ret_JSON = json.dumps({
                     'datasetId':self.__pid,
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
        self.user_info    = {"username":username,"password":password}
        self.LogInfo("initialized SvcSciCat")
        return True

    def __login(self):
        url = self.access_point+"Users/login"
        try:
            r = requests.post(url=url, json=self.user_info, headers=self.headers)
            if r.ok:
                try:
                    token = (r.json()["id"])
                    return (token)
                except Exception:
                    self.LogError('Cannot get user ID from SciCat!')
            else:
                self.LogError('Cannot get Response from SciCat Service')
                self.LogError(r)
                self.LogError(url)
                self.LogError(self.user_info)
        except Exception:
            self.LogError('SciCat Service is not available!')
            self.LogError(url)
            self.LogError(self.user_info)
              

    def login(self):
        return self.__login()

    def __polishPID(self, pid = None):
        if type(pid) is str:
            return pid.replace('/','%2F')
        else:
            return pid

    def setDataset(self, beamtimeId, scanId, rawPID):
        #pid = self.__generateDataset.getPID()
        dataset_json = self.__generateDataset.getDerivedDatasetJSON(beamtimeId = beamtimeId, scanId = scanId, rawPID = rawPID)
        url = self.access_point+'DerivedDatasets?access_token='+self.__login()
        r = requests.post(url=url,json=data_json,headers=self.headers)
        datablock_json = self.__generateDataset.getOrigDatablocksJSON()
        url = self.access_point+'OrigDatablocks?access_token='+self.__login()
        r = requests.post(url=url,json=datablock_json,headers=self.headers)

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






