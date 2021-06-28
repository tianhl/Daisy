from __future__ import print_function
import Daisy
class AlgTomopyFindCenter(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)

    def initialize(self):
        self.data = self.get("DataStore").data()
        self.LogInfo("initialized, Tomopy Find Center of the Projections")
        return True

    def execute(self, input_dataobj, subpixel_accuracy, initual_value, output_dataobj):
        import tomopy
        projs = self.data[input_dataobj]
        if (projs is None):
            self.LogError('Please specific input Projections')
            return False
     
        if (len(projs.shape) != 3):
            self.LogError('The shape of Projections should been 3! here is '+str(projs.shape))
            return False
     
        dataobj = tomopy.find_center_pc(projs[0], projs[-1], tol=subpixel_accuracy, rotc_guess=initual_value)
        self.data[output_dataobj] = dataobj
        return True

    def finalize(self):
        self.LogInfo("finalized")
        return True

