from __future__ import print_function
import Sniper
import sys

class DaisySvc(Sniper.SvcBase):

    def __init__(self, name):
        super().__init__(name)

    def initialize(self):
        pass

    def finalize(self):
        pass

    def get(self,name):
        task = self.getParent()
        # find Python Instances Map
        instance = task.findOperator(name)
        if instance is False:
            # find C++ Instances Map
            instance = task.find("DataMemSvc").find(name)
        return instance

    def setLogLevel(self, level):
        Sniper.setLogLevel(level)

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
