#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     
import Daisy 

init_dict   = {
               'loadtifs':{'class_name':'DataHdlerAlg.LoadTIFs',\
                          },\
              }

cfg_dict   = {'loadtifs':{'input_path':'/home/tianhl/workarea',\
                         },
             }

if __name__ == "__main__":
    wf = Daisy.CreateWorkflowEngine(class_name='PyWorkflowEngine', name='workflow')
    wf.initialize(default_init = init_dict)
    wf.config(default_cfg = cfg_dict)
    wf.setLogLevel(3)
    a=wf.createSvc('PyServices.SvcSciCat/SvcSciCat')

    #aPID='CSTR:17081.11bsrf.3w1.8d8023f166a94b05ba678710d14aff25'
    a.initialize(access_url='http://192.168.14.92:3000/api/v3/', username='analyzer', password='analyzer@2021')
    aPID=a.getPID(beamtimeId='GB14-20210621-19', scanId='scan00003')
    datasetinfo=a.getDatasetInfo(pid=aPID)
    #print(datasetinfo)
    #print(datasetinfo['sourceFolder'])
    #print(datasetinfo['beamtimeId'])
    #print(datasetinfo['scanId'])
    #filelist=a.getDataFileList(pid=pid)
    #print(filelist)
    a.updateDataset('/home/tianhl/workarea/Codes/git-sniper/Daisy/Examples/hello.json')
    a.setDataset(rawPID = aPID, doCommit = False)


    #wf['loadtifs'].execute(startswith='tomo_',seperator='_', idx=2, output_dataobj='tomodat')

    #data = wf.datastore['tomodat']
    #wf['loadtifs'].finalize()
    
    #k = wf.datastore.keys()
    #print(data.dtype)
    #print(k)
    #print(a)
    wf.finalize()
