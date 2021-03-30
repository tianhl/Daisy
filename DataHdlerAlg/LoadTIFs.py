from __future__ import print_function
import numpy as np
import os 
import dxchange
import Daisy

class LoadTIFs(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)
        self.cfg        = {}
        self.ipath      = None

    def initialize(self):
        self.data = self.get("DataStore").data()
        self.LogInfo("initialized")
        #if default_init is not None:
        #    if input_path is None:
        #        if 'input_path' in default_init:
        #            input_path = default_init['input_path']
        #        else:
        #            self.LogError('Please enter Input PATH!')
        #            return False
        #elif input_path is None:
        #    self.LogError('Please enter Input PATH!')
        #    return False
        #self.ipath = input_path


    def config(self, cfgdata=None):
        if cfgdata is None:
            self.LogError('Please provide configuration file!')
        Daisy.CfgParser(self, cfgdata, self.cfg)
        self.ipath = self.cfg['input_path']

        if os.path.isdir(self.ipath):
            self.LogInfo("initialized, read TIF Files in Path: "+self.ipath)
            return True
        else:
            self.LogError('initiallized, Path '+self.ipath+' does not exist')
            return False 

    def execute(self, startswith, seperator, idx, output_dataobj):
        if (startswith is None) or (seperator is None) or (idx is None):
            self.LogError('Please enter scanning requirements for files')
            return False
        filelist = os.listdir(self.ipath)
        filelist = list(filter(lambda filename: filename.startswith(startswith), filelist))
        if len(filelist) == 0:
            self.LogError('Can not scan required files, Please check!')
            return False
        else:    
            filelist.sort()
            self.LogInfo('First Input File: '+filelist[0])
        if not (filelist[0].split('.')[-1].upper() == 'TIF'):
            self.LogError('Files should be TIF')
            return False

        fileidxs=list(map(lambda filename: '.'.join(filename.split('.')[:-1]).split(seperator)[idx], filelist))
        if len(fileidxs) == 0:
            self.LogError('Can not scan required files, Please check!')
            return False
        else:
            self.LogInfo('Get ' + str(len(fileidxs)) + ' files in the Path '+self.ipath)
            
        self.data[output_dataobj] = dxchange.read_tiff_stack(self.ipath+'/'+filelist[0],ind=fileidxs)
        self.LogInfo('Load data '+ output_dataobj+' from '+self.ipath)

        return True

    def finalize(self):
        if self.ipath:
            self.LogInfo("finalized, leave path: "+self.ipath)
        return True

