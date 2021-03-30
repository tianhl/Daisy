from __future__ import print_function
import Daisy 

class AlgFAIIntegrate(Daisy.Base.DaisyAlg):

    import json
    import numpy as np
    import pyFAI

    def __init__(self, name):
        #DaisyAlg.__init__(self, name)
        super().__init__(name)
        self.cfg        = {}
        self.func       = None
        self.wavelength = None
        self.option     = None

    def initialize(self, wavelength=None, option=None, default_init = None):
        if default_init is not None:
            if wavelength is None:
                if 'wavelength' in default_init:
                    wavelength = default_init['wavelength']
                else:
                    wavelength = '1.0'
            if option is None:
                self.LogInfo('alginte option: '+str(option))
                if 'option' in default_init:
                    option = default_init['option']
                else:
                    option = '1D'
                    self.LogInfo('2alginte option: '+str(option))
        else:
            if option is None:
                option = '1D'
            if wavelength is None:
                option = '1.0'
        self.wavelength = wavelength
        self.option = option.upper()
        self.data = self.get("DataStore").data()
        self.ai   = pyFAI.AzimuthalIntegrator(wavelength=self.wavelength)
        if self.option == '1D':
            self.func   = self.ai.integrate1d
        elif self.option == '2D':
            self.func   = self.ai.integrate2d
        elif self.option == 'RADIAL':
            self.func   = self.ai.integrate_radial
        else:
            self.func   = self.ai.integrate1d
        #self.LogInfo("initialized, pyFAI AzimuthalIntegrator("+self.option+") with wavelength "+self.wavelength)
        return True

    def config(self, cfgdata=None):
        if cfgdata is None:
            self.LogError('Please provide configuration file!')
        Daisy.CfgParser(self, cfgdata, self.cfg)
        self.ai.setFit2D(directDist=self.cfg['directDist'], centerX=self.cfg['centerX'], \
                         centerY=self.cfg['centerY'], tilt=self.cfg['tilt'], \
                         tiltPlanRotation=self.cfg['PlanRotation'], pixelX=self.cfg['pixelX'],\
                         pixelY=self.cfg['pixelY'], splineFile=None)
        return True

    def execute(self, input_dataobj, input_maskobj, output_dataobj, unit='2th_deg'):
        expdata   = self.data[input_dataobj]
        caldata   = self.data[input_maskobj]
        ndim      = expdata.shape[0]
        spectrums = np.zeros((ndim,self.cfg['ntth']))
        for idx in range(0,ndim):
            #print(idx)
            theta, spectrums[idx] = self.func(expdata[idx,:,:], self.cfg['ntth'],\
                                         filename=None, correctSolidAngle=True, unit=unit,\
                                         mask=caldata, azimuth_range=(self.cfg['azimin'],self.cfg['azimax']),\
                                         radial_range=(self.cfg['radmin'],self.cfg['radmax']))
        self.data[output_dataobj]={'x':theta,'y':spectrums}
        #self.LogInfo('Integrate('+self.option+') '+input_dataobj+' to '+output_dataobj)

        return True

    #def execute(self, input_dataobj, input_maskobj, output_dataobj, unit='2th_deg'):
    #    kwargs          = {'input_dataobj':input_dataobj, 'input_maskobj':input_maskobj, 'output_dataobj':output_dataobj, 'unit':unit}
    #    input_dataobjs  = self.split(kwargs)
    #    output_dataobjs = {}
    #    for idx, dataobj in enumerate(input_dataobjs):
    #        output_item = self.multi_execute(dataobj,kwargs)
    #        output_dataobjs[idx]=output_item
    #    self.join(output_dataobjs,kwargs)

    #    return True

    def split(self, kwargs):
        #self.LogTest(' split data')
        expdata     = self.data[kwargs['input_dataobj']]
        ndim        = expdata.shape[0]
        ret_dataobj = []
        for idx in range(0,ndim):
            ret_dataobj.append(expdata[idx,:,:])
        return ret_dataobj

    def multi_execute(self, input_dataobj, kwargs):
        #self.LogTest('multiple execute')
        caldata   = self.data[kwargs['input_maskobj']]
        unit      = kwargs['unit']
        theta, spectrum = self.func(input_dataobj, self.cfg['ntth'],\
                                         filename=None, correctSolidAngle=True, unit=unit,\
                                         mask=caldata, azimuth_range=(self.cfg['azimin'],self.cfg['azimax']),\
                                         radial_range=(self.cfg['radmin'],self.cfg['radmax']))
        return {'x':theta, 'y':spectrum}

    def join(self, output_dataobjs, kwargs):
        #self.LogTest('join data')
        output_dataobj   = kwargs['output_dataobj']
        ndim             = len(output_dataobjs)
        spectrums        = np.zeros((ndim,self.cfg['ntth']))
        theta            = None
        for key in output_dataobjs.keys():
            data           = output_dataobjs[key]    
            spectrums[key] = data['y']
            theta          = data['x']
        self.data[output_dataobj]={'x':theta,'y':spectrums}

    def finalize(self):
        self.LogInfo("finalized")
        return True
