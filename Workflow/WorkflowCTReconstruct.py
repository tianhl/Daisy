
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
             'findcenter':{'class_name':'PyAlgorithms.AlgTomopyFindCenter',\
                          },\
            'reconstruct':{'class_name':'PyAlgorithms.AlgTomopyRecon',\
                          },\
               'savedata':{'class_name':'DataHdlerAlg.SaveTIFs',\
                          }\
              }


@Daisy.Base.Singleton
class WorkflowCTReconstruct(Daisy.Base.PyWorkflow):
    def execute(self, projs_file, darks_file, flats_file, idx, initual_center, num_sample, output_name):

        self.engine['loadprojs'].config(cfgdata=projs_file)
        self.engine['loaddarks'].config(cfgdata=darks_file)
        self.engine['loadflats'].config(cfgdata=flats_file)
        self.engine['loadprojs'].execute(input_path='/scan/data/andor_img_shaped_image', output_dataobj='tomodata')
        self.engine['loaddarks'].execute(input_path='/scan/data/andor_img_shaped_image', output_dataobj='darkdata')
        self.engine['loadflats'].execute(input_path='/scan/data/andor_img_shaped_image', output_dataobj='flatdata')
        self.engine['filterdata'].execute(input_dataobj='tomodata', output_dataobj='tomodata_proc', idxs=idx)
        self.engine['filterdata'].execute(input_dataobj='darkdata', output_dataobj='darkdata_proc', idxs=idx)
        self.engine['filterdata'].execute(input_dataobj='flatdata', output_dataobj='flatdata_proc', idxs=idx)
        self.engine['normalize'].execute(projs_dataobj='tomodata_proc', darks_dataobj='darkdata_proc', flats_dataobj='flatdata_proc', output_dataobj='normdata')
        self.engine['angles'].execute(input_dataobj='normdata', output_dataobj='thetas')
        self.engine['minuslog'].execute(input_dataobj='normdata', output_dataobj='mlogdata')
        self.engine['findcenter'].execute(input_dataobj='mlogdata', subpixel_accuracy = 0.5, initual_value= initual_center, output_dataobj='center')
        center = self.get_data('center')
        print('center: '+str(center))
        for i in range(num_sample//2+1):
            c=center-i*0.5
            self.engine['reconstruct'].execute(input_dataobj='mlogdata', theta='thetas',center=c, alg_type='fbp', output_dataobj='recodata')
            odata = self.get_data('recodata')
            for i in range(odata.shape[0]):
                self.engine['savedata'].execute(input_dataobj=odata[i], outputfile_name=output_name+str(c)+'_'+str(i)+'.tif' )
        for i in range(num_sample//2):
            c=center+(i+1)*0.5
            self.engine['reconstruct'].execute(input_dataobj='mlogdata', theta='thetas',center=c, alg_type='fbp', output_dataobj='recodata')
            odata = self.get_data('recodata')
            for i in range(odata.shape[0]):
                self.engine['savedata'].execute(input_dataobj=odata[i], outputfile_name=output_name+'_'+str(c)+'_'+str(i)+'.tif' )

if __name__ == "__main__":
    projs_file = {'inputfile_name':'/hepsfs/bl/3W1/202106/Data/GB14-20210621-19/raw/crystal01/scan02/andor_img_tomo.h5'}
    darks_file = {'inputfile_name':'/hepsfs/bl/3W1/202106/Data/GB14-20210621-19/raw/crystal01/scan02/andor_img_dark.h5'}
    flats_file = {'inputfile_name':'/hepsfs/bl/3W1/202106/Data/GB14-20210621-19/raw/crystal01/scan02/andor_img_flat.h5'}
    scratchdata='/hepsfs/bl/3W1/202106/Data/GB14-20210621-19/scratch/crystal01/scan02/'

    wf = WorkflowCTReconstruct('CTRWF')
    wf.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict)
    wf.execute(projs_file, darks_file, flats_file, idx=[1,500], initual_center = 1012, num_sample=5, output_name=scratchdata+'rec_test')
    wf.finalize()

