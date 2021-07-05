#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     
if __name__ == '__main__':
    import sys
    kernel_json = sys.argv[1]
    print('input kernel access file: '+ kernel_json)
    from DaisyWorkflow_client import DaisyWorkflow_client
    wfc = DaisyWorkflow_client(connection_file = kernel_json)
    wfc.initialize(workflow_cfgfile='hello.json', class_name = 'WorkflowHelloDaisy')
    wfc.execute()
    keys = wfc.algorithm_keys()
    print(keys)
    wfc.finalize()
#
#
#
#
#def loopRec(index):
#
#
#    wfc.get_algorithm('loadtomo').config(cfgdata={'input_path':'/opt/CT/Hidra_7636/tests_00274/pco_edge_01/'})
#    filename = 'testzhangyi'+str(index)+'.h5'
#    wfc.get_algorithm('savedata').config(cfgdata={'outputfile_name':filename})
#    
#    wfc.get_algorithm('loadtomo').execute(startswith='tests_00274', seperator='_', idx=index, output_dataobj='tomodata')
#    wfc.get_algorithm('angles').execute(input_dataobj='tomodata', output_dataobj='thetas')
#    wfc.get_algorithm('minuslog').execute(input_dataobj='tomodata', output_dataobj='logdata')
#    wfc.get_algorithm('reconstruct').execute(input_dataobj='logdata', theta='thetas',center=1030, alg_type='fbp', output_dataobj='recodata')
#    wfc.get_algorithm('savedata').execute(input_dataobj='recodata', output_path='/entry/reco' )
#
#
#
#
#
#for i in range(512):
#    loopRec(i)
#
#keys = wfc.data_keys()
#print(keys)
