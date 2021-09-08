from __future__ import print_function
import Daisy

import gi
gi.require_version('Ufo', '0.0')
from gi.repository import Ufo
import numpy as np
import math

class AlgUFORecon(Daisy.Base.DaisyAlg):


    def __init__(self, name):
        super().__init__(name)

    def initialize(self):
        self.data    = self.get("DataStore").data()
        self.graph   = Ufo.TaskGraph()
        self.sched   = Ufo.Scheduler()

        manager = Ufo.PluginManager()
        self.read = manager.get_task('memory-in')
        self.sino = manager.get_task('transpose-projections')
        self.pad  = manager.get_task('pad')
        self.fft  = manager.get_task('fft')
        self.fltr = manager.get_task('filter')
        self.ifft = manager.get_task('ifft')
        self.bp   = manager.get_task('backproject')
        self.crop = manager.get_task('crop')
        self.write= manager.get_task('memory-out')
        self.LogInfo("initialized, UFO Reconstruction")
        return True

    def execute(self, input_dataobj, theta, center, alg_type, output_dataobj):
        projs  = self.data[input_dataobj]
        thetas = self.data[theta]
        if (projs is None):
            self.LogError('Please specific input Projections')
            return False
     
        if (len(projs.shape) != 3):
            self.LogError('The shape of Projections should been 3! here is '+str(projs.shape))
            return False

        input_size_x = projs.shape[0] 
        input_size_y = projs.shape[1] 
        input_size_z = projs.shape[2] 

        self.read.props.pointer = projs.__array_interface__['data'][0]
        self.read.props.height  = input_size_x 
        self.read.props.width   = input_size_y 
        self.read.props.number  = input_size_z 
        self.sino.props.number  = input_size_z

        try:
            bitdepth = int(str(projs.dtype)[-2:])
            self.read.props.bitdepth = bitdepth
        except e:
            self.LogError(e)
            return False

        
        output_size_x  = int(math.sqrt(2)*input_size_x)
        output_size_y  = input_size_z
        output_size_z  = input_size_y

        padding_x = 2 ** int(math.ceil(math.log(2 * output_size_x, 2))) - output_size_x
        padding_y = 0
        self.pad.props.width  = output_size_x + padding_x
        self.pad.props.height = output_size_y + padding_y
        self.pad.props.x      = padding_x/2
        self.pad.props.y      = padding_y/2
        self.pad.props.addressing_mode = 'clamp_to_edge'

        self.fft.set_properties(dimensions=1)
        self.ifft.set_properties(dimensions=1)
        self.fltr.set_properties(filter='ramp-fromreal')

        if (thetas is None):
            self.LogError('Please specific input thetas')
            return False
     
        if (len(thetas.shape) != 1):
            self.LogError('The shape of thetas should been 1! here is '+str(projs.shape))
            return False

        if (len(thetas) != projs.shape[0] ):
            self.LogError('The dimention of thetas should been equ to the number of projections! here is '+str(projs.shape))
            return False

        self.bp.props.angle_step = abs(float(thetas[0])-float(thetas[-1]))/len(thetas)
        self.bp.props.angle_offset = thetas[0]
        self.bp.set_properties(center+padding_x)
        
        self.crop.props.width  = output_size_x
        self.crop.props.height = output_size_y
        self.crop.props.x      = padding_x/2
        self.crop.props.y      = padding_y/2

        slides = np.zeros((output_size_x, output_size_y, output_size_z), dtype=np.float32)
        self.write.props.pointer  = slides.__array_interface__['data'][0]
        self.write.props.max_size = slides.nbytes

        self.graph.connect_nodes(read, sino)
        self.graph.connect_nodes(sino, pad)
        self.graph.connect_nodes(pad,  fft)
        self.graph.connect_nodes(fft,  fltr)
        self.graph.connect_nodes(fltr, ifft)
        self.graph.connect_nodes(ifft, bp)
        self.graph.connect_nodes(bp,   crop)
        self.graph.connect_nodes(crop, write)
        self.sched.run(graph) 

        self.data[output_dataobj] = slides
        return True

    def finalize(self):
        self.LogInfo("finalized")
        return True

