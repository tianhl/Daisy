from __future__ import print_function
import Daisy

class SaveTIFs(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)
        self.cfg        = {}

    def initialize(self, outputfile_name = None, default_init = None):
        self.data   = self.get("DataStore").data()
        self.LogInfo("initialized")
    
    def config(self, cfgdata=None):
        #if cfgdata is None:
        #    self.LogError('Please provide configuration file!')
        #Daisy.CfgParser(self, cfgdata, self.cfg)
        #self.foname = self.cfg['outputfile_name']
        return True

    def execute(self, input_dataobj, outputfile_name=''):
        import numpy as np
        from PIL import Image
        #idata  = self.data[input_dataobj]
        idata  = input_dataobj
        dtype  = type(idata)

        im = Image.fromarray(idata, mode='F')
        im.save(outputfile_name, 'TIFF')
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
        self.LogInfo("finalized")
        return True
