from __future__ import print_function
import numpy as np
import Daisy 

class AlgSelectSinogram(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)

    def initialize(self):
        self.data = self.get("DataStore").data()
        self.LogInfo("initialized, Selecte Sinograms")
        return True

    def execute(self, input_dataobj, output_dataobj, idxs ):
        projections = self.data[input_dataobj]
        if (projections is None):
            self.LogError('Please specific input Projections')
            return False
     
        if (len(projections.shape) != 3):
            self.LogError('The shape of Projections should been 3! here is '+str(projections.shape))
            return False
     
        size = projections.shape[1]
        if size < len(idxs):
            self.LogError('Size of Selected Sinogram Exceeds!')
            return False

        idxs=np.array(idxs)
        if idxs.dtype == int:
            idxs.sort()
        if (idxs[0]<0)or(idxs[-1]>=size):
            self.LogError('Indexs of Selected Sinogram Exceed!')
            return False

     
        group = np.zeros((projections.shape[0],len(idxs),projections.shape[2]),projections.dtype)
        for cid, col in enumerate(idxs):
            for idx in range(projections.shape[0]):
                group[idx][cid]=projections[idx,col,:]   
        

        self.data[output_dataobj] = group
        self.data[output_dataobj+'_idxs'] = idxs
        return True

    def finalize(self):
        self.LogInfo("finalized")
        return True

