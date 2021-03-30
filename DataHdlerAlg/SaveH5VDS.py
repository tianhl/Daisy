from __future__ import print_function
import numpy as np
import h5py
import hdf5plugin
import Daisy

class SaveH5VDS(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)
        self.cfg     = {}
        self.__idxs  = {}
        self.__shape = None
        self.__dtype = None
        self.__opath = None

    def initialize(self, default_init = None):

        self.data   = self.get("DataStore").data()
        return True

    def config(self, cfgdata=None):
        if cfgdata is None:
            self.LogError('Please provide configuration file!')
        Daisy.CfgParser(self, cfgdata, self.cfg)
        self.foname = self.cfg['outputfile_name']
        self.dspath = self.cfg['hdf5dataset_path']
        return True
   
    def execute(self, input_dataobj, index, outputfile_name = None, output_path=''):
        idata  = input_dataobj
        #idata  = self.data[input_dataobj]
        dtype  = idata.dtype
        shape  = idata.shape
        try:
            index = int(index)
        except:
            self.LogError('Can not convert the index ' + index + ' into integrate')

        self.LogInfo('type  of ouput data: '+str(dtype))
        self.LogInfo('shape of ouput data: '+str(shape))
        if self.__shape == None:
            self.__shape = shape
        if self.__shape != shape:
            self.LogError('The shape of dataobj is not consistent, current shape is ' \
                           + str(shape) + ', and previous shape is ' + str(self.__shape))
            return False

        if self.__dtype == None:
            self.__dtype = dtype
        if self.__dtype != dtype:
            self.LogError('The dtype of dataobj is not consistent, current dtype is ' \
                           + str(dtype) + ', and previous dtype is ' + str(self.__dtype))
            return False

        if self.__opath == None:
            self.__opath = output_path
        if self.__opath != output_path:
            self.LogError('The path dataobj is not consistent, current path is ' \
                           + str(output_path) + ', and previous path is ' + str(self.__opath))
            return False

        with h5py.File(outputfile_name, "w") as f:
            #d = f.create_dataset(output_path, (100,), str(dtype), idata)
            d = f.create_dataset(output_path, self.__shape, self.__dtype, idata)

        self.__idxs[index]=outputfile_name

        self.LogInfo('Save data '+output_path+' in '+outputfile_name)

        return True

    def finalize(self):
        vds_shape = (len(self.__idxs),)+self.__shape

        # Assemble virtual dataset
        layout = h5py.VirtualLayout(shape=vds_shape, dtype=self.__dtype)
        for key in self.__idxs.keys():
            filename = self.__idxs[key]
            vsource = h5py.VirtualSource(filename, self.__opath, shape=self.__shape)
            layout[key] = vsource



        with h5py.File(self.foname, "w", libver="latest") as f:
            f.create_virtual_dataset(self.dspath, layout, fillvalue=-5)
        self.LogInfo("finalized, close HDF5 File: "+self.foname)
        return True
