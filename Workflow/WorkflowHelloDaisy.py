from __future__ import print_function
import Daisy 

class WorkflowHelloDaisy(Daisy.Base.PyWorkflow):
    def execute(self):
        self.engine['helloDaisy'].execute()

