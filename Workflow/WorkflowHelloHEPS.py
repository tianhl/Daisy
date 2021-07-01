from __future__ import print_function
import Daisy 

class WorkflowHelloHEPS(Daisy.Base.PyWorkflow):
    def execute(self):
        self.engine['helloheps'].execute()

