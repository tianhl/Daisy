from __future__ import print_function

import Daisy
class AlgHelloDaisy(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)

    def config(self):
        pass

    def initialize(self):
        self.LogInfo("initialized, Hello Daisy ")
        return True

    def execute(self):
        self.LogInfo("execute, Hello Daisy ")
        return True

    def finalize(self):
        self.LogInfo("finalize, Hello Daisy ")
        return True






