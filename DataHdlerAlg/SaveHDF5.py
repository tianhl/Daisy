from __future__ import print_function
import numpy as np
import h5py
import hdf5plugin
import Daisy

class SaveHDF5(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)
        self.cfg        = {}

    def initialize(self, outputfile_name = None, default_init = None):
        self.data   = self.get("DataStore").data()
        self.LogInfo("initialized")
    
    def config(self, cfgdata=None):
        if cfgdata is None:
            self.LogError('Please provide configuration file!')
        Daisy.CfgParser(self, cfgdata, self.cfg)
        self.foname = self.cfg['outputfile_name']
        return True

    def execute(self, input_dataobj, output_path=''):
        idata  = self.data[input_dataobj]
        dtype  = type(idata)
        print('type of ouput data: '+str(dtype))
        with h5py.File(self.foname, 'w') as hfile:
            hfile.create_dataset(output_path, data=idata)
            self.LogInfo('Save data '+input_dataobj+' as '+output_path+' to '+self.foname)
       # if type(output_path) is str:
       #     items = output_path.split('/')
       #     for item in items:
       #         if len(item) == 0:
       #             continue
       #         if item in handle.keys():
       #             handle = handle[item]
       #         else:
       #             handle = handle.create_group(item)
       #         print('enter path: '+ item)
       #                
       # if dtype is dict: 
       #     for key in idata.keys():
       #         if type(key) is str:
       #             self.LogInfo(key+" is stored in file "+self.foname)
       #             self.LogInfo(str(idata[key]))
       #             handle.create_dataset(key, data=idata[key])
       #         else:
       #             self.LogError("The keys of input data should be class <'str'> ")
       #             return True
       # else:
       #     print('================='+output_path)
       #     handle.create_dataset(output_path, data=idata)
       # 

        return True

    def finalize(self):
        #self.hdf5.close()
        self.LogInfo("finalized, close HDF5 File: "+self.foname)
        return True
