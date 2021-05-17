#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     
import Daisy 

init_dict   = {
               'loadtifs':{'class_name':'DataHdlerAlg.LoadTIFs',\
                          },\
              }

cfg_dict   = {'loadtifs':{'input_path':'/opt/CT/ZY-2/',\
                         },
             }

if __name__ == "__main__":
    wf = Daisy.CreateWorkflowEngine(class_name='PyWorkflowEngine', name='workflow')
    wf.initialize(default_init = init_dict)
    wf.config(default_cfg = cfg_dict)
    wf.setLogLevel(3)
    a=wf.createSvc('PyServices.SvcSciCat/SvcSciCat')


    #wf['loadtifs'].execute(startswith='dark_',seperator='_', idx=1, output_dataobj='tomodat')
    wf['loadtifs'].execute(startswith='tomo_',seperator='_', idx=1, output_dataobj='tomodat')

    data = wf.datastore['tomodat']
    wf['loadtifs'].finalize()
    
    k = wf.datastore.keys()
    print(data.dtype)
    print(k)
    print(a)
    wf.finalize()
