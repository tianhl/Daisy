import Daisy.Base.DaisyAlg as DaisyAlg 
import Daisy

#class PyWorkflow(Daisy.Base.DaisyAlg):
class PyWorkflow(DaisyAlg):
    def __init__(self, name):
        super().__init__(name)

    def initialize(self, workflow_engine=None, default_init = None, workflow_environment={}, algorithms_cfg={}):
        #print(self.objName()+' workflow_environment type of '+str(type(workflow_environment))+" value: "+str(workflow_environment))
        #print(self.objName()+' default_init type of '+str(type(default_init))+" value: "+str(default_init))
        if default_init is not None:
            if workflow_engine is None:
                if 'workflow_engine' in default_init:
                    workflow_engine = default_init['workflow_engine']
                else:
                    self.LogError('Please enter Workflow Engine name!')
            if 'workflow_environment' in default_init:
               workflow_environment = default_init['workflow_environment']
        elif workflow_engine is None:
            self.LogError('Please enter Workflow Engin name!')

        self.engine = Daisy.CreateWorkflowEngine(class_name=workflow_engine, name=self.objName())
        self.engine.initialize(default_init=workflow_environment)
        self.engine.config(default_cfg=algorithms_cfg)
        
    
    def data_keys(self):
        return list(self.engine.datastore.keys())

    def algorithm_keys(self):
        return self.engine.keys()

    def get_data(self, data_name):
        return self.engine.datastore[data_name]

    def get_algorithm(self, algorithm_name):
        return self.engine[algorithm_name]

    def execute(self):
        raise Exception('Must')

    def finalize(self):
        self.engine.finalize()
