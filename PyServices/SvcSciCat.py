from __future__ import print_function

import Daisy
import requests
import json
class SvcSciCat(Daisy.Base.DaisySvc):

    class GenerateDataset:
        def __init__(self, pidprefix='CSTR:17081.11bsrf.3w1.'):
            self.__datafile_list = []
            self.__datafile_size = 0
            self.__folder        = None
            self.__worker_name   = 'Daisy'
            self.__pid           = pidprefix

        def reset(self):
            self.__datafile_list = []
            self.__datafile_size = 0
            self.__folder        = None

        def __getCheckSum(self, filename):
            from hashlib import md5
            with open(filename, 'rb') as f:
                s = md5(f.read()).hexdigest()
                return s

        def addFile(self, filename=''):
            import os 
            from datetime import datetime
            if os.path.exists(filename) == False:
                return False
            filename = os.path.abspath(filename)
            filesize = os.path.getsize(filename)
            filetime = datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%Y-%m-%dT%H:%M:%S.%f")
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

            self.__datafile_size = self.__datafile_size + filesize
            if self.__folder == None:
                self.__folder = os.path.split(filename)[0]
            elif self.__folder is not os.path.split(filename)[0]:
                self.LogError('Cannot change folder')
               
            #if (self.__datafile_size + 1) == len(self.__datafile_list):
            #    self.__datafile_size = self.__datafile_size + 1
            #else:
            #    print('Warning: update file')
            #    self.__datafile_size = len(self.__datafile_list)

        def getPID(self):
            return self.__pid

        def getDerivedDatasetJSON(self, raw_info):
            import datetime
            ret_JSON = {
                           "investigator": raw_info["principalInvestigator"],
                           "inputDatasets": [
                             raw_info['pid']
                           ],
                           "usedSoftware": [
                             "Daisy"
                           ],
                           "jobParameters": {},
                           "jobLogData": "string",
                           "pid": self.__pid,
                           "beamtimeId": raw_info['beamtimeId'],
                           "scanId": raw_info['scanId'],
                           "owner": raw_info['owner'],
                           "ownerEmail": raw_info["ownerEmail"],
                           "orcidOfOwner": "string",
                           "contactEmail": raw_info["contactEmail"],
                           "sourceFolder": self.__folder,
                           "size":self.__datafile_size,
                           "packedSize": 0,
                           "creationTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
                           "type": "derived",
                           "validationStatus": "unvalidated",
                           "keywords": [
                             "string"
                           ],
                           "description": raw_info["description"],
                           "datasetName": raw_info["datasetName"]+'-Daisy',
                           "classification": raw_info["classification"],
                           "license": "string",
                           "version": "string",
                           "ownerGroup": "string",
                           "accessGroups": [
                             "string"
                           ],
                           "createdBy": "string",
                           "updatedBy": "string",
                           "createdAt": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
                           "updatedAt": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),

                          }

            return ret_JSON


        def getOrigDatablocksJSON(self):

            ret_JSON = {
                     'datasetId':self.__pid,
                     'size':self.__datafile_size,
                     'dataFileList':self.__datafile_list
                     }
            return ret_JSON

    def __init__(self, name):
        super().__init__(name)
        self.headers           = {"Content-Type": "application/json;charset=UTF-8"}
        self.__generateDataset = self.GenerateDataset()
        self.__filesnum        = 0
        pass

    def initialize(self, access_url='http://192.168.14.92:3000/api/v3/' , username='admin', password='ihep123'):
        self.access_point = access_url 
        self.user_info    = {"username":username,"password":password}
        self.__token      = self.__login()
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
                    self.LogError(r.text)
            else:
                self.LogError('Cannot get Response from SciCat Service')
                self.LogError(r)
                self.LogError(url)
                self.LogError(self.user_info)
        except Exception:
            self.LogError('SciCat Service is not available!')
            self.LogError(url)
            self.LogError(self.user_info)
              

    def getToken(self):
        return self.__token

    def __polishPID(self, pid = None):
        if type(pid) is str:
            return pid.replace('/','%2F')
        else:
            return pid

    def setDataset(self, rawPID, doCommit = False):

        rawDatasetinfo=self.getDatasetInfo(pid=rawPID)

        dataset_json = self.__generateDataset.getDerivedDatasetJSON(raw_info=rawDatasetinfo)
        dataset_url = self.access_point+'DerivedDatasets?access_token='+self.__token

        datablock_json = self.__generateDataset.getOrigDatablocksJSON()
        datablock_url = self.access_point+'OrigDatablocks?access_token='+self.__token

        pid = self.__generateDataset.getPID()
        ret = {
              'beamtimeId'  : dataset_json['beamtimeId'],
              'pid'         : pid,
              'path'        : dataset_json['sourceFolder'],
              'status'      : 1,
              'filenumber1' : self.__filesnum,
        }
        if(doCommit):
            r = requests.post(url=dataset_url,json=dataset_json,headers=self.headers)
            r = requests.post(url=datablock_url,json=datablock_json,headers=self.headers)
            self.LogInfo('Commit Derived Dataset ' + pid + ' to SciCat')
            self.__generateDataset.reset()
            self.__filesnum = 0
            return ret
        else:
            self.LogInfo('Ready to Commit Derived Dataset ' + pid + ' to SciCat')
            print(dataset_url)
            print(dataset_json)
            print(datablock_url)
            print(datablock_json)
            return ret

    def updateDataset(self, filename):
        self.__generateDataset.addFile(filename) 
        self.__filesnum = self.__filesnum + 1

    def getDatasetInfo(self, pid = None):
        pid=self.__polishPID(pid)  
        url = self.access_point+'Datasets/'+pid+'?access_token='+self.__token
        self.LogInfo(url)
        r=requests.get(url=url,json=self.user_info,headers=self.headers)
        return (r.json())
  
    def getPID(self, beamtimeId, scanId):
        url = self.access_point+'Datasets/findOne?filter={"where":{"scanId":"'+scanId+'","beamtimeId":"'+beamtimeId+'"}}&access_token='+self.__token
        self.LogInfo(url)
        r=requests.get(url=url,json=self.user_info,headers=self.headers)
        pid = r.json()['pid']
        return pid

    def getDataFileList(self, pid = None):
        pid=self.__polishPID(pid)  
        url = self.access_point+'OrigDatablocks/findOne?filter={"where":{"datasetId":"'+pid+'"}}&access_token='+self.__token
        self.LogInfo(url)
        r=requests.get(url=url,json=self.user_info,headers=self.headers)
        
        return  tuple(eachfile['path'] for eachfile in r.json()['dataFileList'])

    def execute(self):
        self.LogInfo("execute SvcSciCat, Hello Daisy ")
        return True

    def finalize(self):
        self.LogInfo("finalize SvcSciCat, Hello Daisy ")
        return True






