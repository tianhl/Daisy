#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     
import Daisy 

init_dict   = {
                'loadtomo':{'class_name':'DataHdlerAlg.LoadTIFs',\
                          },\
                'loaddark':{'class_name':'DataHdlerAlg.LoadTIFs',\
                          },\
                'loadflat':{'class_name':'DataHdlerAlg.LoadTIFs',\
                          },\
                'loadreco':{'class_name':'DataHdlerAlg.LoadHDF5',\
                          },\
             'filterdata':{'class_name':'PyAlgorithms.AlgSelectSinogram',\
                          },\
              'normalize':{'class_name':'PyAlgorithms.AlgTomopyNormalize',\
                          },\
                 'angles':{'class_name':'PyAlgorithms.AlgTomopyAngles',\
                          },\
               'minuslog':{'class_name':'PyAlgorithms.AlgTomopyMinuslog',\
                          },\
            'reconstruct':{'class_name':'PyAlgorithms.AlgTomopyRecon',\
                          },\
               'savedata':{'class_name':'DataHdlerAlg.SaveHDF5',\
                          }\
              }


cfg_dict    = {
              'loadtomo':{'input_path':'/opt/CT/ZY-2/'},
              'loaddark':{'input_path':'/opt/CT/ZY-2/'},
              'loadflat':{'input_path':'/opt/CT/ZY-2/'},
              'loadreco':{'inputfile_name':'/opt/CT/ZY-2/tomopy_reco.h5'},
              'savedata':{'outputfile_name':'tomopy_scan.h5'},
}


@Daisy.Base.Singleton
class CTRecWorkflow(Daisy.Base.PyWorkflow):
    def execute(self):

        #self.engine['loadhdf5'].execute(input_path='/entry/tomo', output_dataobj='tomodata')
        #self.engine['loadhdf5'].execute(input_path='/entry/dark', output_dataobj='darkdata')
        #self.engine['loadhdf5'].execute(input_path='/entry/flat', output_dataobj='flatdata')
        #self.engine['loadreco'].execute(input_path='/entry/reco', output_dataobj='recondata')
        self.engine['loadtomo'].execute(startswith='tomo_',seperator='_', idx=2, output_dataobj='tomodata')
        self.engine['loaddark'].execute(startswith='dark_',seperator='_', idx=1, output_dataobj='darkdata')
        self.engine['loadflat'].execute(startswith='flat_',seperator='_', idx=1, output_dataobj='flatdata')
        self.engine['filterdata'].execute(input_dataobj='tomodata', output_dataobj='tomodata_proc', idxs=[1,2])
        self.engine['filterdata'].execute(input_dataobj='darkdata', output_dataobj='darkdata_proc', idxs=[1,2])
        self.engine['filterdata'].execute(input_dataobj='flatdata', output_dataobj='flatdata_proc', idxs=[1,2])
        self.engine['normalize'].execute(projs_dataobj='tomodata_proc', darks_dataobj='darkdata_proc', flats_dataobj='flatdata_proc', output_dataobj='normdata')
        #self.engine['normalize'].execute(projs_dataobj='tomodata', darks_dataobj='darkdata', flats_dataobj='flatdata', output_dataobj='normdata')
        self.engine['angles'].execute(input_dataobj='normdata', output_dataobj='thetas')
        self.engine['minuslog'].execute(input_dataobj='normdata', output_dataobj='mlogdata')
        self.engine['reconstruct'].execute(input_dataobj='mlogdata', theta='thetas',center=1030, alg_type='fbp', output_dataobj='recodata')
        self.engine['savedata'].execute(input_dataobj='tomodata', output_path='/entry/tomo' )
        self.engine['savedata'].execute(input_dataobj='darkdata', output_path='/entry/dark' )
        self.engine['savedata'].execute(input_dataobj='flatdata', output_path='/entry/flat' )
        self.engine['savedata'].execute(input_dataobj='recodata', output_path='/entry/reco' )

if __name__ == "__main__":
    wf = CTRecWorkflow('CTRecWorkflow')
    wf.setLogLevel(5)
    #wf.setLogFile('log.log')
    #wf.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict, algorithms_cfg = cfg_dict)
    wf.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict)
    #wf2 = CTRecWorkflow('CTRecWorkflow')
    #wf2.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict)
    #print('wf0:', str(wf))
    #print('wf1:', str(wf2))
    wf.get_algorithm('loadtomo').config({'input_path':'/opt/CT/ZY-2/'})
    wf.get_algorithm('loaddark').config({'input_path':'/opt/CT/ZY-2/'})
    wf.get_algorithm('loadflat').config({'input_path':'/opt/CT/ZY-2/'})
    wf.get_algorithm('savedata').config({'outputfile_name':'tomopy_scan.h5'})
    wf.execute()
    data =wf.data_keys()
    print(data)
    #algs =wf.algorithm_keys()
    #wf.get_algorithm('loadmask')
    #wf.get_data('result'))

    wf.finalize()
