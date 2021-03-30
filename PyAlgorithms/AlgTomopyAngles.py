from __future__ import print_function
import Daisy

class AlgTomopyAngles(Daisy.Base.DaisyAlg):


    def __init__(self, name):
        super().__init__(name)

    def initialize(self):
        self.data = self.get("DataStore").data()
        self.LogInfo("initialized, Tomopy Get Angles")
        return True

    def execute(self, input_dataobj, output_dataobj):
        import tomopy
        projs = self.data[input_dataobj]
        if (projs is None):
            self.LogError('Please specific input Projections')
            return False
     
        if (len(projs.shape) != 3):
            self.LogError('The shape of Projections should been 3! here is '+str(projs.shape))
            return False
     
        dataobj = tomopy.angles(projs.shape[0])
        self.data[output_dataobj] = dataobj
        return True

    def finalize(self):
        self.LogInfo("finalized")
        return True

