#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     
import Daisy 

init_dict   = {
               'loadtifs':{'class_name':'DataHdlerAlg.LoadTIFs',\
                          },\
               'savedata':{'class_name':'DataHdlerAlg.SaveH5VDS',\
                          }\
              }

cfg_dict   = {'loadtifs':{'input_path':'/hepsfs/huy/Data/ZY-1/tomo',\
                         },
              'savedata':{'outputfile_name':'andor_img_example.h5',\
                          'hdf5dataset_path':'data',\
                         }\
             }

if __name__ == "__main__":
    wf = Daisy.CreateWorkflowEngine(class_name='PyWorkflowEngine', name='workflow')
    wf.initialize(default_init = init_dict)
    wf.config(default_cfg = cfg_dict)
    wf.setLogLevel(3)


    #wf['loadtifs'].execute(startswith='dark_',seperator='_', idx=1, output_dataobj='tomodat')
    wf['loadtifs'].execute(startswith='tomo_',seperator='_', idx=1, output_dataobj='tomodat')

    data = wf.datastore['tomodat']
    print(data.shape)
    for i in range(data.shape[1]):
        odata = data[:,i,:]
        #foname = 'andor_ima_shaped_image_vds_'+str(i)+'.h5'
        foname = 'vds_'+str(i)+'.h5'
        #wf['savedata'].execute(input_dataobj=odata, index=i, outputfile_name=foname, output_path='/scan/data/andor_img_shaped_image')
        wf['savedata'].execute(input_dataobj=odata, index=i, outputfile_name=foname, output_path='scan')

    wf['loadtifs'].finalize()
    wf['savedata'].finalize()
    
    k = wf.datastore.keys()
    print(data.dtype)
    print(k)
    wf.finalize()
