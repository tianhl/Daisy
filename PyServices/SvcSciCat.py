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
            self.__prefix        = pidprefix
            self.__pid           = self.__prefix

        def reset(self):
            self.__datafile_list = []
            self.__datafile_size = 0
            self.__folder        = None
            self.__pid           = self.__prefix

        def __getCheckSum(self, filename):
            from hashlib import md5
            with open(filename, 'rb') as f:
                s = md5(f.read()).hexdigest()
                return s
            return None

        def addFile(self, filename=''):
            import os 
            from datetime import datetime, timedelta
            if os.path.exists(filename) == False:
                print(filename + " does not exist!")
                return False
            filename = os.path.abspath(filename)
            filesize = os.path.getsize(filename)
            #filetime = datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            filetime = (datetime.fromtimestamp(os.path.getmtime(filename))+timedelta(hours=-8)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
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
                print('Cannot change folder')
                return False

            return True 
            #if (self.__datafile_size + 1) == len(self.__datafile_list):
            #    self.__datafile_size = self.__datafile_size + 1
            #else:
            #    print('Warning: update file')
            #    self.__datafile_size = len(self.__datafile_list)

        def getPID(self):
            return self.__pid

        def getDerivedDatasetJSON(self, raw_info):
            import datetime
            try:
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
            except Exception:
                print('Can not generate dataset json')
                return None

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

    def setDataset(self, rawPID = None, doCommit = False):

        if rawPID == None:
            self.LogError('Please specify input pid')
            return None

        rawDatasetinfo=self.getDatasetInfo(pid=rawPID)
        if rawDatasetinfo == None:
            self.LogError('Can not get Raw Dataset Information with pid '+ rawPID)
            return False

        dataset_json = self.__generateDataset.getDerivedDatasetJSON(raw_info=rawDatasetinfo)
        if dataset_json == None:
            self.LogError('Can not generate Dataset JSON')
            return None
        dataset_url = self.access_point+'DerivedDatasets?access_token='+self.__token

        datablock_json = self.__generateDataset.getOrigDatablocksJSON()
        datablock_url = self.access_point+'OrigDatablocks?access_token='+self.__token
        if datablock_json['size'] == 0 or len(datablock_json['dataFileList']) == 0: 
            self.LogError('No new file added to the dataset')
            self.LogError(str(datablock_json))
            return False

        pid = self.__generateDataset.getPID()
        ret = {
              'beamtimeId'  : dataset_json['beamtimeId'],
              'pid'         : pid,
              'path'        : dataset_json['sourceFolder'],
              'status'      : 1,
              'filenumber1' : self.__filesnum,
              'type'        : 'derived',
        }
        if(doCommit):

            try:
                r = requests.post(url=dataset_url,json=dataset_json,headers=self.headers)
                if not r.ok:
                    self.LogError('Cannot post Dataset to SciCat')
                    self.LogError(r.text)
                    self.LogError(dataset_url)
                    self.LogError(dataset_json)
                    return False
            except Exception:
                self.LogError('SciCat Service is not available!')
                self.LogError(dataset_url)
                return False
  
            try:
                r = requests.post(url=datablock_url,json=datablock_json,headers=self.headers)
                if not r.ok:
                    self.LogError('Cannot post Datablock to SciCat')
                    self.LogError(r.text)
                    self.LogError(datablock_url)
                    self.LogError(datablock_json)
                    return False
            except Exception:
                self.LogError('SciCat Service is not available!')
                self.LogError(datablock_url)
                return False
  
            self.LogInfo('Commit Derived Dataset ' + pid + ' to SciCat')
            self.__generateDataset.reset()
            self.__filesnum = 0
            return ret
        else:
            self.LogInfo('Ready to Commit Derived Dataset ' + pid + ' to SciCat')
            #self.__generateDataset.reset()
            #self.__filesnum = 0
            print(dataset_url)
            print(dataset_json)
            print(datablock_url)
            print(datablock_json)
            return ret

    def updateDataset(self, filename):
        self.__generateDataset.addFile(filename) 
        self.__filesnum = self.__filesnum + 1

    def getDatasetInfo(self, pid = None):

        if pid == None:
            self.LogError('Please specify pid')
            return None

        pid=self.__polishPID(pid)  
        url = self.access_point+'Datasets/'+pid+'?access_token='+self.__token
        self.LogInfo(url)

        try:
            r = requests.get(url=url,json=self.user_info,headers=self.headers)
            if r.ok:
                try:
                    return (r.json())
                except Exception:
                    self.LogError('Cannot get Dataset from SciCat with PID '+ PId)
                    self.LogError(r.text)
                    return None
            else:
                self.LogError('Cannot get Response from SciCat Service')
                self.LogError(r)
                self.LogError(url)
                self.LogError(self.user_info)
                return None
        except Exception:
            self.LogError('SciCat Service is not available!')
            self.LogError(url)
            self.LogError(self.user_info)
            return None
  
    def getPID(self, beamtimeId = None, scanId = None):

        if beamtimeId == None or scanId == None:
            self.LogError('Please specify beamtimeId and scanId')
            return None

        url = self.access_point+'Datasets/findOne?filter={"where":{"scanId":"'+scanId+'","beamtimeId":"'+beamtimeId+'"}}&access_token='+self.__token
        self.LogInfo(url)
        try:
            r = requests.get(url=url,json=self.user_info,headers=self.headers)
            if r.ok:
                try:
                    pid = (r.json()["pid"])
                    return pid
                except Exception:
                    self.LogError('Cannot get PID from SciCat with BeamtimeID '+ beamtimeId + ' ScanID ' + scanId)
                    self.LogError(r.text)
                    return None
            else:
                self.LogError('Cannot get Response from SciCat Service')
                self.LogError(r)
                self.LogError(url)
                self.LogError(self.user_info)
                return None
        except Exception:
            self.LogError('SciCat Service is not available!')
            self.LogError(url)
            self.LogError(self.user_info)
            return None

    def getDataFileList(self, pid = None):
        if pid == None:
            self.LogError('Please specify pid')
            return None
        pid=self.__polishPID(pid)  
        url = self.access_point+'OrigDatablocks/findOne?filter={"where":{"datasetId":"'+pid+'"}}&access_token='+self.__token
        self.LogInfo(url)

        try:
            r = requests.get(url=url,json=self.user_info,headers=self.headers)
            if r.ok:
                try:
                    datafile_list = (r.json()["dataFileList"])
                    files = tuple(eachfile['path'] for eachfile in datafile_list)
                    return files
                except Exception:
                    self.LogError('Cannot get filelist from SciCat with PID '+ pid)
                    self.LogError(r.text)
                    return None
            else:
                self.LogError('Cannot get Response from SciCat Service')
                self.LogError(r)
                self.LogError(url)
                self.LogError(self.user_info)
                return None
        except Exception:
            self.LogError('SciCat Service is not available!')
            self.LogError(url)
            self.LogError(self.user_info)
            return None

    def execute(self):
        self.LogInfo("execute SvcSciCat, Hello Daisy ")
        return True

    def finalize(self):
        self.LogInfo("finalize SvcSciCat, Hello Daisy ")
        return True






