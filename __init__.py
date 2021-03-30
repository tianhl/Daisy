print('==================================================')
print('===   Daisy: Data Analysis Interated System    ===')
print('==================================================')
print('===     To see a world in a grain of sand      ===')
print('===       And a heaven in a wild flower        ===')
print('===  Hold infinity in the palm of your hand    ===')
print('===          And eternity in an hour           ===')
print('===                                            ===')
print('===                        by William Blake    ===')
print('==================================================')

import Daisy.Base as Base
import Daisy.DataHdlerAlg as DataHdlerAlg
import Daisy.PyAlgorithms as PyAlgorithms
def CreateWorkflowEngine(class_name='PyWorkflowEngine', name=None):
    if name is None:
        name = class_name
    return getattr(Base, class_name)(name)

def CfgParser(instance, cfgdata, cfgobj=None):
    import json
    cfg = {}
    if type(cfgdata) is str:
        try:
            cfg = json.loads(cfgdata)
        except BaseException as error:
            instance.LogError(error)
            return False
    elif type(cfgdata) is dict:
        cfg=cfgdata
    else:
        instance.LogError('Can not load configuration data!')
        return False
    
    if cfgobj is None:
        return cfg
    else:
        for key in cfg.keys():
            if type(key) is str:
                cfgobj[key]=cfg[key]
                #self.property(key).set(self.cfg[key])
            else:
                instance.LogError("The keys of configuration should be class <'str'> ")
