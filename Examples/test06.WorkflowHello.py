#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: tianhl

# using the new Workflow Engine for data analysis.
     

init_dict   = {
               'helloDaisy':{'class_name':'PyAlgorithms.AlgHelloDaisy',\
                          },\
              }

import Daisy


if __name__ == "__main__":
    wf = Daisy.Workflow.WorkflowHelloDaisy('HelloDaisyWorkflow')
    wf.initialize(workflow_engine='PyWorkflowEngine', workflow_environment = init_dict)
    wf.execute()
    alg =wf.algorithm_keys()
    print('algs in workflow')
    print(alg)

    wf.finalize()
