#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

# using the new Mgr.

import Sniper

if __name__ == "__main__":

    Sniper.setLogLevel(2)
    Sniper.setColorful(2)
    #Sniper.setShowTime(True)

    task = Sniper.Task("task")
    task.setEvtMax(3)

    from Sniper import PyDataStore
    task.createSvc("PyDataStoreSvc/DataStore")

    #import HelloWorld
    import SniperCoreUsages
    task.createAlg("HelloWorld/SetAlg")

    x = task.find("SetAlg")
    print("Before setting properties")
    x.show()


    x.property("VarBool").set(True)
    x.property("VecFloat").set([0.01])
    x.property("PairDVD").set([0.09, [1.1, 2.2, 3.3]])
    x.property("MapIntStr").set({1: 'str1'})
    print("After setting properties")
    x.show()


    z = task.createAlg("HelloWorld/GetAlg")

    task.show()

    task.run()
