#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     
import Daisy 

init_dict   = {
               'ls' :{'class_name':'PyAlgorithms.AlgCommandline' },\
               'pwd':{'class_name':'PyAlgorithms.AlgCommandline' },\
              }

cfg_dict   = { 
               'ls':{'shell_command':'ls' },\
               'pwd':{'shell_command':'pwd' },\
             }

if __name__ == "__main__":
    wf = Daisy.CreateWorkflowEngine(class_name='PyWorkflowEngine', name='workflow')
    wf.initialize(default_init = init_dict)
    wf.config(default_cfg = cfg_dict)
    wf.setLogLevel(3)


    wf['pwd'].execute()
    wf['ls'].execute(parameters=['-al'])

    wf.finalize()
