from __future__ import print_function
import Sniper

class DaisyAlg(Sniper.PyAlgBase):

    def __init__(self, name):
        Sniper.PyAlgBase.__init__(self, name)

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

