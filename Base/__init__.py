from .PyWorkflowEngine   import PyWorkflowEngine
from .PyMQWorkflowEngine import PyMQWorkflowEngine
from .DaisyAlg           import DaisyAlg
from .PyWorkflow         import PyWorkflow
#from Daisy.Base.PyWorkflowEngine   import PyWorkflowEngine
#from Daisy.Base.PyMQWorkflowEngine import PyMQWorkflowEngine
#from Daisy.Base.DaisyAlg           import DaisyAlg
#
#from HEPS.WorkflowHelloHEPS       import WorkflowHelloHEPS
#from HEPS.WorkflowCTReconstruct   import WorkflowCTReconstruct
#from HEPS.HEPSWorkflow_client     import HEPSWorkflow_client


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
