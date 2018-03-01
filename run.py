'''
Created on 19 FEB. 2018

@author: AYB
'''

import multiprocessing
from multiprocessing.managers import SyncManager
from queue import PriorityQueue
import signal
from time import sleep
import sys
import os
import Logger
import DCMController, AMSpiServer, ServosController, USController, MainAUC, AgentController
import redis

log = Logger.RCLog('MainAUC')
class MyManager(SyncManager):
    pass
MyManager.register("PriorityQueue", PriorityQueue)  # Register a shared PriorityQueue


def mgr_init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    log.debug('initialized manager')

def run_DCMController():
    DCMController.main()
def run_AMSpiServer():
    AMSpiServer.main()
def run_ServosController():
    ServosController.main()

def run_USController():
    USController.main()
def run_MainUC():
    MainAUC.main()
def run_AgentController():
    AgentController.main()


if __name__ == '__main__':
    # Save a reference to the original signal handler for SIGINT.
    default_handler = signal.getsignal(signal.SIGINT)
    # Set signal handling of SIGINT to ignore mode.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    #multiprocessing.set_start_method('spawn')
    processes = []
    manager = MyManager()
    manager.start(mgr_init)
    #in_queue = multiprocessing.Queue(30)
    #out_queue = multiprocessing.Queue(20)
    #priority_queue = manager.PriorityQueue(20)
    dcmc_process = multiprocessing.Process(target=run_DCMController)
    dcmc_process.daemon = True
    dcmc_process.start()
    processes.append(dcmc_process)
    #------------------------
    dsc_process = multiprocessing.Process(target=run_ServosController)
    dsc_process.daemon = True
    dsc_process.start()
    processes.append(dsc_process)
    #------------------------
    ams_process = multiprocessing.Process(target=run_AMSpiServer)
    ams_process.daemon = True
    ams_process.start()
    processes.append(ams_process)
    #------------------------
    usc_process = multiprocessing.Process(target=run_USController)
    usc_process.daemon = True
    usc_process.start()
    processes.append(usc_process)
    #------------------------
    mauc_process = multiprocessing.Process(target=run_MainUC)
    mauc_process.daemon = True
    mauc_process.start()
    processes.append(mauc_process)
    #------------------------
    ac_process = multiprocessing.Process(target=run_AgentController)
    ac_process.daemon = True
    ac_process.start()
    processes.append(ac_process)
    #===========================================================================
    # cam_process = multiprocessing.Process(target=cam_loop,args=(in_queue, ))
    # cam_process.daemon = True
    # lock = multiprocessing.Lock()
    # out_queue_cond = multiprocessing.Condition(lock)
    # cam_process.start()
    # processes.append(cam_process)
    # predict_process = multiprocessing.Process(target=predict,args=(in_queue, priority_queue, ))
    # predict_process.daemon = True
    # predict_process.start()
    # processes.append(predict_process)
    # 
    # coord_process = multiprocessing.Process(target=coord,args=(priority_queue, out_queue, ))
    # coord_process.daemon = True
    # coord_process.start()
    # processes.append(coord_process)
    #===========================================================================
    
    
    
    # Since we spawned all the necessary processes already, 
    # restore default signal handling for the parent process. 
    signal.signal(signal.SIGINT, default_handler)
    try:
        
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        log.error("AYB: caught KeyboardInterrupt, killing processes")
        broker = redis.StrictRedis()
        broker.publish('DCMC', '{"action": "exit",  "speed": "0", "time_limit": "0"}')
        broker.publish('SC', '{"action": "exit",  "angle": "-1"}')
        broker.publish('US', '{"action": "exit", "distance": "0"}')
        sleep(1)
        for process in processes:
            process.terminate()
        manager.shutdown() 
    finally:
        manager.shutdown()    