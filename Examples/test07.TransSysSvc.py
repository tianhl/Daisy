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
    a=wf.createSvc('PyServices.SvcTransSys/DataTrans')

    dataset_summary = {
             'beamtimeId': 'GB14-20210621-19', 
             'pid': 'CSTR:17081.11bsrf.3w1.d835427c40da46daaab96c796eada5c3', 
             'path': '/hepsfs/bl/3W1/202106/Data/GB14-20210621-19/processed', 
             'status': 1, 
             'filenumber1': 1,
             'type':'derived',
             }
    a.initialize(host='192.168.212.204', user='root', password='123456_123', port=3306, db='HEPSbed', charset='utf8')
    a.execute(table='dataset_list', data=dataset_summary, doCommit=False)

    wf.finalize()
