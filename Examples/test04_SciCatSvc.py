#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     
import Daisy 

init_dict   = {
               'loadtifs':{'class_name':'DataHdlerAlg.LoadTIFs',\
                          },\
              }

cfg_dict   = {'loadtifs':{'input_path':'/hepsfs/huy/Data/ZY-2/',\
                         },
             }

if __name__ == "__main__":
    wf = Daisy.CreateWorkflowEngine(class_name='PyWorkflowEngine', name='workflow')
    wf.initialize(default_init = init_dict)
    wf.config(default_cfg = cfg_dict)
    wf.setLogLevel(3)
    a=wf.createSvc('PyServices.SvcSciCat/SvcSciCat')

    a.initialize(access_url='http://192.168.14.92:3000/api/v3/', username='analyzer', password='analyzer@2021')
    pid=a.getPID(beamtimeId='GB14-20210621-19', scanId='scan02')
    datasetinfo=a.getDatasetInfo(pid=pid)
    filelist=a.getDataFileList(pid=pid)
    tomofiles = [f for f in filelist if f.find('tomo')>0]
    print([f for f in filelist if f.find('flat')>0])
    print([f for f in filelist if f.find('dark')>0])
    print(tomofiles)
    a.updateDataset('/hepsfs/bl/3W1/202106/Data/GB14-20210621-19/scratch/crystal01/scan02/rec_test1027.25_0.tif')
    a.setDataset()


    #wf['loadtifs'].execute(startswith='tomo_',seperator='_', idx=2, output_dataobj='tomodat')

    #data = wf.datastore['tomodat']
    #wf['loadtifs'].finalize()
    
    #k = wf.datastore.keys()
    #print(data.dtype)
    #print(k)
    #print(a)
    wf.finalize()
