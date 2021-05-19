from __future__ import print_function
import Daisy
import subprocess

class AlgCommandline(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)
        self.__shell = subprocess
        self.cfg     = {}

    def initialize(self):
        #self.data = self.get("DataStore").data()
        self.LogInfo("initialized, Tomopy Reconstruction")
        return True


    def config(self, cfgdata=None):
        if cfgdata is None:
            self.LogError('Please provide configuration file!')
        Daisy.CfgParser(self, cfgdata, self.cfg)
        self.cmd = self.cfg['shell_command']
        ret = self.__shell.run(['which', self.cmd], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if ret.returncode == 0: 
            self.LogInfo("Find "+ self.cmd + ' at ' + ret.stdout.decode()[:-1])
            return True
        else:
            self.LogError("Can not find "+ self.cmd + ' error message: ' + ret.stderr.decode()[:-1])
            return False
   
    def execute(self, parameters = None):
        execute_cmd = [self.cmd]
        if parameters and type(parameters) == list:
            for item in parameters:
                if type(item) == str:
                    execute_cmd.append(item)
        
        ret = self.__shell.run(execute_cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if ret.returncode == 0: 
            self.LogInfo("Execute "+ self.cmd + ' with parameters: ' + str(parameters))
            self.LogInfo(ret.stdout.decode()[:-1])
            return True
        else:
            self.LogError("Can not find "+ self.cmd + ' error message: ' + ret.stderr.decode()[:-1])
            return False
   

        return True

    def finalize(self):
        self.LogInfo("finalized")
        return True

