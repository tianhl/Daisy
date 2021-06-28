from __future__ import print_function
import Daisy
import numpy as np

class AlgMatrixTranspose(Daisy.Base.DaisyAlg):

    def __init__(self, name):
        super().__init__(name)

    def initialize(self):
        self.data = self.get("DataStore").data()
        self.LogInfo("initialized, Matrix Transpose")
        return True

    def execute(self, input_dataobj, output_dataobj, transpose=()):
        matrix_orig = self.data[input_dataobj]
        if(len(matrix_orig.shape)!=len(transpose)):
            self.LogError('Dimention of Transpose is NOT consistent with the Dimention of Matrix')
            return False

        try:
           self.data[output_dataobj]=matrix_orig.transpose(transpose)
        except Exception as ex:
           self.LogError(str(ex))
           return False

        return True

    def finalize(self):
        self.LogInfo("finalized")
        return True

