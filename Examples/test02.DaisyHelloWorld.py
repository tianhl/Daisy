#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

# using the new Mgr.

import Daisy 

init_dict   = {
               'helloDaisy':{'class_name':'PyAlgorithms.AlgHelloDaisy',\
                          },\
              }


if __name__ == "__main__":

    wf = Daisy.CreateWorkflowEngine(class_name='PyWorkflowEngine', name='workflow')
    wf.initialize(default_init = init_dict)
    wf['helloDaisy'].execute()
