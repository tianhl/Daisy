import sys
import Sniper
from Daisy.Base import PyMQDataStore


class PyMQWorkflowEngine(Sniper.ExecUnit):

    def __init__(self, name):
        Workflow.__init__(self, name)
        Sniper.setColorful(2)
        Sniper.setLogLevel(2)
        self.__pyAlgHolder=[]
        self.__algList=[]
        self.operators = {}


    def findOperator(self, name):
        if name in self.operators:
            return self.operators[name]
        else:
            return False

    def __getitem__(self, key):
        self.LogTest('find alg: '+key)
        return self.findAlg(key)
            #return self.find(key).execute # return function object, and execute it

    def scatter(self, algname, kwargs):
        pass
        import queue
        import threading
        # data split and local data initialization
        instance       = self[algname]
        input_dataobjs = instance.split(kwargs)
        output_dataobjs= {}
        input_queue    = queue.Queue()
        output_queue   = queue.Queue()
        threads        = []
       
        # thread and queue
        def worker():
            while True:
                try:
                    idx, input_item = input_queue.get(block=False)
                except queue.Empty:
                    break
                #import random, time
                #rnd = random.random()
                #time.sleep(rnd)
                #self.LogTest(str(threading.get_ident())+' worker works for idx: '+str(idx)+' with sleep: '+str(rnd))
                output_item = instance.multi_execute(input_item,kwargs)
                output_queue.put((idx, output_item))
                input_queue.task_done()
 
        for idx, dataobj in enumerate(input_dataobjs):
            input_queue.put((idx, dataobj))
            self.LogTest('scattering dataobj idx: '+str(idx))
        for idx in range(10):
            t = threading.Thread(target=worker)
            self.LogTest('Threads starts ')
            t.start()
            threads.append(t)

        # block until all tasks are done
        input_queue.join()
        for t in threads:
            t.join()

        # collection and reduction
        while True:
            try:
                idx, output_item = output_queue.get(block=False)
            except queue.Empty:
                break
            self.LogTest('collecting dataobj idx: '+str(idx))
            output_dataobjs[idx]=output_item
            output_queue.task_done()

        output_queue.join()
        instance.join(output_dataobjs,kwargs)
            

    def initialize(self, default_init=None):
        #self.addSvc(datasvc)
        #self.createSvc("PyDataStoreSvc/Operators")
        self.snoopy = self.Snoopy()
        self.snoopy.config()
        self.snoopy.initialize()

        #p=PyMQDataStore.PyMQDataStore('DataStore')
        #self.operators['DataStore'] = p
        #self.datastore = p.data()
        
        self.operators['DataStore'] = PyMQDataStore.PyMQDataStore('DataStore')
        self.datastore = self.operators['DataStore'].data()
        
        if default_init is not None:
            init_cfg = HEPS.CfgParser(self, default_init)
            for key in init_cfg.keys():
                alg_name  = key
                alg_class = init_cfg[key]['class_name']
                alg = self.createAlg(alg_class+'/'+alg_name)
                try:
                    algParas = init_cfg[key]['init_paras']
                    self[alg_name].initialize(default_init=algParas)
                except KeyError as error:
                    self.LogDebug(error)

    def config(self, default_cfg=None):
        if default_cfg is not None:
            cfg = HEPS.CfgParser(self, default_cfg)
            for key in cfg.keys():
                self.LogTest(key+' configure with dict '+str(cfg[key]))
                self[key].config(cfg[key])

    def keys(self):
        return self.__algList

    def addAlg(self, alg, isPyAlg = True):
        super().addAlg(alg)
        if isPyAlg is True:
            self.__pyAlgHolder.append(alg)
        
    def createAlg(self, name):
        items   = name.split('/')
        clsname = items[0]
        algname = items[0]
        isPyAlg = False
        if len(items) == 2:
            algname = items[1]

        try:
            alg = getattr(HEPS, clsname)(algname)
            isPyAlg = True
            self.addAlg(alg, isPyAlg)
            self.__algList.append(algname)
            return alg
        except AttributeError as error:
            self.LogDebug(error)
            self.property("algs").append(name)
            print('create alg: '+name)
            self.__algList.append(algname)
            isPyAlg = False
            return self[algname]
        return False
        #self.operators[algname] = alg

    def run(self):
        pass

    def finalize(self):
        for key in self.operators.keys():
            print('stop '+ str(key))
            self.operators[key].finalize()
        self.snoopy.finalize()

    def _log(self, level, flag, msgs):
        if ( self.logLevel() <= level):
            prefix = self.scope() + self.objName() + '.' + sys._getframe(2).f_code.co_name
            print("%-30s" % prefix, flag, end='')
            for msg in msgs:
                print(msg, end='')
            print()

    def LogTest(self, *msgs):
        self._log(0,  " TEST: ", msgs)

    def LogDebug(self, *msgs):
        self._log(2,  "DEBUG: ", msgs)

    def LogInfo(self, *msgs):
        self._log(3,  " INFO: ", msgs)

    def LogWarn(self, *msgs):
        self._log(4,  " WARN: " , msgs)

    def LogError(self, *msgs):
        self._log(5,  "ERROR: ", msgs)

    def LogFatal(self, *msgs):
        self._log(6,  "FATAL: ", msgs)
