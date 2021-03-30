from __future__ import print_function
import Daisy

class AlgTomopyRecon(Daisy.Base.DaisyAlg):


    def __init__(self, name):
        super().__init__(name)

    def initialize(self):
        self.data = self.get("DataStore").data()
        self.LogInfo("initialized, Tomopy Reconstruction")
        return True

    def execute(self, input_dataobj, theta, center, alg_type, output_dataobj):
        import tomopy
        projs  = self.data[input_dataobj]
        thetas = self.data[theta]
        if (projs is None):
            self.LogError('Please specific input Projections')
            return False
     
        if (len(projs.shape) != 3):
            self.LogError('The shape of Projections should been 3! here is '+str(projs.shape))
            return False

        if (thetas is None):
            self.LogError('Please specific input thetas')
            return False
     
        if (len(thetas.shape) != 1):
            self.LogError('The shape of thetas should been 1! here is '+str(projs.shape))
            return False

        if (len(thetas) != projs.shape[0] ):
            self.LogError('The dimention of thetas should been equ to the number of projections! here is '+str(projs.shape))
            return False

        dataobj = tomopy.recon(projs, thetas, center=center, algorithm=alg_type)
        self.data[output_dataobj] = dataobj
        return True

    def finalize(self):
        self.LogInfo("finalized")
        return True

