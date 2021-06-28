
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.

import Daisy

init_dict   = {
               'loadprojs':{'class_name':'DataHdlerAlg.LoadHDF5',\
                          },\
               'loaddarks':{'class_name':'DataHdlerAlg.LoadHDF5',\
                          },\
               'loadflats':{'class_name':'DataHdlerAlg.LoadHDF5',\
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
              'loadprojs':{'inputfile_name':'/hepsfs/bl/3W1/202106/data/GB14-20210621-11/raw/crystal01/scan02/andor_img_tomo.h5'},\
              'loaddarks':{'inputfile_name':'/hepsfs/bl/3W1/202106/data/GB14-20210621-11/raw/crystal01/scan02/andor_img_dark.h5'},\
              'loadflats':{'inputfile_name':'/hepsfs/bl/3W1/202106/data/GB14-20210621-11/raw/crystal01/scan02/andor_img_flat.h5'},\
               'savedata':{'outputfile_name':'tomopy_scan.h5'},
}


@Daisy.Base.Singleton
class CTRecWorkflow(Daisy.Base.PyWorkflow):
    def execute(self):

        self.engine['loadprojs'].execute(input_path='/scan/data/andor_img_shaped_image', output_dataobj='tomodata')
        self.engine['loaddarks'].execute(input_path='/scan/data/andor_img_shaped_image', output_dataobj='darkdata')
        self.engine['loadflats'].execute(input_path='/scan/data/andor_img_shaped_image', output_dataobj='flatdata')
        #self.engine['filterdata'].execute(input_dataobj='tomodata', output_dataobj='tomodata_proc', idxs=[1,2])
        #self.engine['filterdata'].execute(input_dataobj='darkdata', output_dataobj='darkdata_proc', idxs=[1,2])
        #self.engine['filterdata'].execute(input_dataobj='flatdata', output_dataobj='flatdata_proc', idxs=[1,2])
        #self.engine['normalize'].execute(projs_dataobj='tomodata_proc', darks_dataobj='darkdata_proc', flats_dataobj='flatdata_proc', output_dataobj='normdata')
        #self.engine['normalize'].execute(projs_dataobj='tomodata', darks_dataobj='darkdata', flats_dataobj='flatdata', output_dataobj='normdata')
        #self.engine['angles'].execute(input_dataobj='normdata', output_dataobj='thetas')
        self.engine['angles'].execute(input_dataobj='tomodata', output_dataobj='thetas')
        #self.engine['minuslog'].execute(input_dataobj='normdata', output_dataobj='mlogdata')
        self.engine['minuslog'].execute(input_dataobj='tomodata', output_dataobj='mlogdata')
        #self.engine['reconstruct'].execute(input_dataobj='mlogdata', theta='thetas',center=1030, alg_type='fbp', output_dataobj='recodata')
        #self.engine['savedata'].execute(input_dataobj='recodata', output_path='/entry/reco' )

if __name__ == "__main__":
    wf = CTRecWorkflow('CTRecWorkflow')
    wf.setLogLevel(5)
    #wf.setLogFile('log.log')
    wf.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict, algorithms_cfg = cfg_dict)
    #wf.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict)
    #wf2 = CTRecWorkflow('CTRecWorkflow')
    #wf2.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict)
    #print('wf0:', str(wf))
    #print('wf1:', str(wf2))
    #wf.get_algorithm('loadtomo').config({'input_path':'/opt/CT/ZY-2/'})
    #wf.get_algorithm('loaddark').config({'input_path':'/opt/CT/ZY-2/'})
    #wf.get_algorithm('loadflat').config({'input_path':'/opt/CT/ZY-2/'})
    #wf.get_algorithm('savedata').config({'outputfile_name':'tomopy_scan.h5'})
    wf.execute()
    data =wf.data_keys()
    print(data)
    #algs =wf.algorithm_keys()
    #wf.get_algorithm('loadmask')
    #wf.get_data('result'))

    wf.finalize()

