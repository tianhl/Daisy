from __future__ import print_function
from HEPS import PyWorkflow

class WorkflowHelloHEPS(PyWorkflow):
    def execute(self):
        self.engine['helloheps'].execute()

