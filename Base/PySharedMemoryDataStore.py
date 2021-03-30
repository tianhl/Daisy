import numpy as np
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager
import pickle
class PySharedMemoryDataStore():


    class DataStoreSMM:
        def __int__(self, mgr):
            self.__mgr  = mgr
            self.__data = {}

        def __getitem__(self, key, isInfo = False):
            access_info = self.__data[key]
            if isInfo：
                val = pickle.dumps(access_info)
            else:
                shm = SharedMemory(access_info['name'])
                val = np.ndarray(access_info['shape'], dtype=access_info['dtype'], buffer=shm.buf)
            return val

        def __setitem__(self, key, value):
            shm = self.__mgr.SharedMemory(size=value.nbytes)
            buf = np.ndarray(value.shape, dtype=value.dtype, buffer=shm.buf)
            buf = value
            self.__data[key] = {'name':shm.name,'shape':value.shape,'dtype':value.dtype}

        def keys():
            return self.__data.keys()

    def __init__(self, name):
        self.__class = 'PySharedMemoryDataStore'
        self.__name  = name
        self.__mgr   = SharedMemoryManager()
        self.__mgr.start()
        self.__smm   = self.DataStoreSMM(self.__mgr)


    def data(self):
        return self.__smm

    def finalize(self):
        #print('datastore stop')
        self.__mgr.shutdown()
