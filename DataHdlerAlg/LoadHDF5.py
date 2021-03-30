from __future__ import print_function
import numpy as np
import h5py
import hdf5plugin
import Daisy

class LoadHDF5(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        #DaisyAlg.__init__(self, name)
        super().__init__(name)
        self.cfg   = {}
        self.hdf5  = None
        self.fname = None

    def initialize(self):
        self.data = self.get("DataStore").data()
        self.LogInfo("initialized")


    def config(self, cfgdata=None):
        if cfgdata is None:
            self.LogError('Please provide configuration file!')
        Daisy.CfgParser(self, cfgdata, self.cfg)
        self.finame = self.cfg['inputfile_name']
        #with h5py.File(self.finame, 'r') as handle:
        #    print(handle)
        #    self.hdf5 = handle
        #    self.LogInfo("initialized, read HDF5 File: "+self.finame)
        #return True

        #if default_init is not None:
        #    if inputfile_name is None:
        #        if 'inputfile_name' in default_init:
        #            inputfile_name = default_init['inputfile_name']
        #        else:
        #            self.LogError('Please enter Input File name!')
        #elif inputfile_name is None:
        #    self.LogError('Please enter Input File name!')
        #self.finame = inputfile_name
        self.hdf5 = h5py.File(self.finame, 'r')
        self.LogInfo("initialized, read HDF5 File: "+self.finame)
        return True

    def execute(self, input_path, output_dataobj):
        self.LogInfo('Load data '+input_path+' as '+output_dataobj+' from '+self.finame)
        #with self.hdf5[input_path] as dataobj:
        #    self.data[output_dataobj] = np.array(dataobj)
        self.data[output_dataobj] = np.array(self.hdf5[input_path])

        return True

    def finalize(self):
        if self.hdf5 and self.finame:
            self.hdf5.close()
            self.LogInfo("finalized, close HDF5 File: "+self.finame)
        return True
