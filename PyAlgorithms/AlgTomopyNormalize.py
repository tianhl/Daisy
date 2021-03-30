from __future__ import print_function
import Daisy
class AlgTomopyNormalize(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)

    def initialize(self):
        self.data = self.get("DataStore").data()
        self.LogInfo("initialized, Tomopy Normalization")
        return True

    def execute(self, projs_dataobj, darks_dataobj, flats_dataobj, output_dataobj):
        import tomopy
        projs = self.data[projs_dataobj]
        darks = self.data[darks_dataobj]
        flats = self.data[flats_dataobj]
        if (projs is None):
            self.LogError('Please specific input Projections')
            return False
     
        if (len(projs.shape) != 3):
            self.LogError('The shape of Projections should been 3! here is '+str(projs.shape))
            return False
     
        if (darks is None):
            self.LogError('Please specific input Darks Data')
            return False
     
        if (len(darks.shape) != 3):
            self.LogError('The shape of Darks Data should been 3! here is '+str(flats.shape))
            return False
     
        if (flats is None):
            self.LogError('Please specific input Flats Data')
            return False
     
        if (len(flats.shape) != 3):
            self.LogError('The shape of Flats Data should been 3! here is '+str(flats.shape))
            return False
     
        dataobj = tomopy.normalize(projs, flats, darks)
        self.data[output_dataobj] = dataobj
        return True

    def finalize(self):
        self.LogInfo("finalized")
        return True

