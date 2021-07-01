#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     
import Daisy 

init_dict   = {
                'loadtomo':{'class_name':'LoadTIFs',\
                          },\
                'loaddark':{'class_name':'LoadTIFs',\
                          },\
                'loadflat':{'class_name':'LoadTIFs',\
                          },\
                'loadreco':{'class_name':'LoadHDF5',\
                          },\
             'filterdata':{'class_name':'AlgSelectSinogram',\
                          },\
              'normalize':{'class_name':'AlgTomopyNormalize',\
                          },\
                'angles':{'class_name':'AlgTomopyAngles',\
                          },\
                'minuslog':{'class_name':'AlgTomopyMinuslog',\
                          },\
             'reconstruct':{'class_name':'AlgTomopyRecon',\
                          },\
               'savedata':{'class_name':'SaveHDF5',\
                          'init_paras':{'outputfile_name':'tomopy_scan.h5'}\
                          }\
              }


cfg_dict    = {
              'loadtomo':{'input_path':'/opt/CT/ZY-2/'},
              'loaddark':{'input_path':'/opt/CT/ZY-2/'},
              'loadflat':{'input_path':'/opt/CT/ZY-2/'},
              'loadreco':{'inputfile_name':'/opt/CT/ZY-2/tomopy_reco.h5'}
}
#cfg_dict   = {'azintalg':{'directDist':169,\
#                          'centerX':1049.967,\
#                          'centerY':1063.892,\
#                          'pixelX':75,\
#                          'pixelY':75,\
#                          'PlanRotation':64.66877,\
#                          'tilt':0.3753,\
#                          'azimin':93,\
#                          'azimax':115,\
#                          'radmin':10.0,\
#                          'radmax':20,\
#                          'ntth':40}\
#             }
#


@Daisy.Singleton
class WorkflowCTReconstruct(Daisy.Base.PyWorkflow):

    def execute(self):

        pass
        #self.engine['loadhdf5'].execute(input_path='/entry/tomo', output_dataobj='tomodata')
        #self.engine['loadhdf5'].execute(input_path='/entry/dark', output_dataobj='darkdata')
        #self.engine['loadhdf5'].execute(input_path='/entry/flat', output_dataobj='flatdata')
        #self.engine['loadreco'].execute(input_path='/entry/reco', output_dataobj='recondata')
        #self.engine['loadtomo'].execute(startswith='tomo_',seperator='_', idx=2, output_dataobj='tomodata')
        #self.engine['loaddark'].execute(startswith='dark_',seperator='_', idx=1, output_dataobj='darkdata')
        #self.engine['loadflat'].execute(startswith='flat_',seperator='_', idx=1, output_dataobj='flatdata')
        #self.engine['filterdata'].execute(input_dataobj='tomodata', output_dataobj='tomodata_proc', idxs=[1,2])
        #self.engine['filterdata'].execute(input_dataobj='darkdata', output_dataobj='darkdata_proc', idxs=[1,2])
        #self.engine['filterdata'].execute(input_dataobj='flatdata', output_dataobj='flatdata_proc', idxs=[1,2])
        #self.engine['normalize'].execute(projs_dataobj='tomodata_proc', darks_dataobj='darkdata_proc', flats_dataobj='flatdata_proc', output_dataobj='normdata')
        #self.engine['normalize'].execute(projs_dataobj='tomodata', darks_dataobj='darkdata', flats_dataobj='flatdata', output_dataobj='normdata')
        #self.engine['angles'].execute(input_dataobj='normdata', output_dataobj='thetas')
        #self.engine['minuslog'].execute(input_dataobj='normdata', output_dataobj='mlogdata')
        #self.engine['reconstruct'].execute(input_dataobj='mlogdata', theta='thetas',center=1030, alg_type='fbp', output_dataobj='recodata')
        #self.engine['savedata'].execute(input_dataobj='tomodata', output_path='/entry/tomo' )
        #self.engine['savedata'].execute(input_dataobj='darkdata', output_path='/entry/dark' )
        #self.engine['savedata'].execute(input_dataobj='flatdata', output_path='/entry/flat' )
        #self.engine['savedata'].execute(input_dataobj='recodata', output_path='/entry/reco' )

if __name__ == "__main__":
    wf = WorkflowCTReconstruct('WorkflowCTReconstruct')
    wf.setLogLevel(5)
    #wf.setLogFile('log.log')
    #wf.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict, algorithms_cfg = cfg_dict)
    wf.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict)
    wf.get_algorithm('loadtomo').config({'input_path':'/opt/CT/ZY-2/'})
    wf.get_algorithm('loaddark').config({'input_path':'/opt/CT/ZY-2/'})
    wf.get_algorithm('loadflat').config({'input_path':'/opt/CT/ZY-2/'})
    wf.get_algorithm('loadreco').config({'inputfile_name':'/opt/CT/ZY-2/tomopy_reco.h5'})
    wf.execute()
    data =wf.data_keys()
    algs =wf.algorithm_keys()
    #wf.get_algorithm('loadmask')
    #wf.get_data('result'))

    wf.finalize()
