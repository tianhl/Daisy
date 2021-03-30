import queue
import threading
import time
import random
import uuid

#class PyMQDataStore(IDataBlock):
class PyMQDataStore():

    class DataStoreQueue:
        def __init__(self, req_q, idx):
            self.__queue = queue.Queue()
            self.__req_queue = req_q
            self.__id = idx

        def __getitem__(self, key):
            self.__req_queue.put((self.__id, key, None))
            ret_key, ret_value = self.__queue.get(block=True)
            if ret_key is key:
                return ret_value
            else:
                print('error')

        def __setitem__(self, key, value):
            self.__req_queue.put((self.__id, key,value))

        def queue(self):
            return self.__queue

    def __init__(self, name):
        self.__name = name
        self.__req_queue = queue.Queue()
        self.__queues  = {}
        self.__running = True
        self.__server  = threading.Thread(target=self.__run)
        self.__server.start()
        self.__datastore = {}

    def __run(self):
        while self.__running:
            try:
                idx, key,value = self.__req_queue.get(block=False)
            except queue.Empty:
                time.sleep(0.01)
                continue
            #print('idx: '+str(idx)+' key: '+str(key)+ ' of '+ str(type(key)) + ' value: '+str(value))
            if value is None:
                # get value
                ret = self.__datastore[key]
                self.__queues[idx].queue().put((key, ret))
            else:
                # set value
                self.__datastore[key] = value

    def data(self):
        idx = uuid.uuid1()
        self.__queues[idx] = self.DataStoreQueue(self.__req_queue, idx)
        #print('new datastore client idx: ' + str(idx))
        return self.__queues[idx]

    def finalize(self):
        #print('datastore stop')
        self.__running = False
        self.__server.join()
        del self.__req_queue
        del self.__datastore
        del self.__queues
