from jupyter_client  import BlockingKernelClient
from random import randint

class DaisyAlgorithm_client:
     def __init__(self, client, code):
         self.alg_access = code 
         self.kc = client
         print('Remote Alg: '+ code)
     def config(self, *args, **kwargs):
         temp_name = 'cfg_dict' + str(randint(1,1000000))
         print(kwargs.keys())
         print(kwargs['cfgdata'])
         if 'cfgdata' in kwargs.keys() and type(kwargs['cfgdata']) == dict:
             cmd = temp_name + " = " + str(kwargs['cfgdata'])
             msg_id  = self.kc.execute(cmd)
             cmd = self.alg_access + ".config(cfgdata= " + temp_name + ")"
             msg_id  = self.kc.execute(cmd)
             cmd = 'del ' + temp_name
             msg_id  = self.kc.execute(cmd)
 
             
     def execute(self, *args, **kwargs):
         print(kwargs.keys())
         cmd = self.alg_access + ".execute("
         for arg in kwargs:
             if type(kwargs[arg]) == str:        
                 cmd = cmd + str(arg) + '= "' + str(kwargs[arg]) + '",'
             else:
                 cmd = cmd + str(arg) + '=' + str(kwargs[arg]) + ','
         cmd = cmd[:-1] + ')'
         self.kc.execute_interactive(cmd)
#        def initialize
#        def finalize


class DaisyWorkflow_client:
    def __init__(self, connection_file = None, executable = False):
        import os
        self.alg_keys = []
        self.dat_keys = []
        #super().__init__()
        self.kc = BlockingKernelClient()
        if connection_file == None:
            raise Exception('Please Specific Connection file to Remote IPython Kernel first')
        if os.access(connection_file, os.R_OK) == False:
            raise Exception('The connection file can no be read!')
        self.kc.load_connection_file(connection_file)
        try:
            self.kc.start_channels()
        except RuntimeError:
            raise Exception('Can not start channels, Please CHECK REMOTE KERNEL STATUS')
        self.executable = executable
        self.remote_name = None
        self.alg_clients = {}

    def initialize(self, class_name = None, workflow_name = None, workflow_cfgfile = None, algorithms_cfgfile = None):
        import os, json
        if class_name == None:
            raise Exception('Please Specific Workflow class name first')
        cmd = "from Daisy.Base import "+class_name
        self.kc.execute_interactive(cmd )
        if workflow_name == None:
            workflow_name = class_name
        self.remote_name = workflow_name
        cmd = self.remote_name + " = " + class_name + "('" + workflow_name + "')"
        self.kc.execute_interactive(cmd )

        if workflow_cfgfile == None:
            raise Exception('Please Specific Workflow Config file first')
        if os.access(workflow_cfgfile, os.R_OK) == False:
            raise Exception('The Workflow Config file can no be read!')

        with open(workflow_cfgfile,'r') as json_file:
            string = json_file.read()
            wf_cfg = json.loads(string)

        temp_name = 'cfg_dict' + str(randint(1,1000000))
        cmd       = temp_name + ' = ' + str(wf_cfg)
        self.kc.execute_interactive(cmd)

        cmd = self.remote_name + ".initialize(workflow_engine='PyWorkflowEngine', workflow_environment = "+ temp_name +")"
        self.kc.execute_interactive(cmd)
        self.kc.execute_interactive('del '+ temp_name)
        
    
    def setLogLevel(self, level):
        pass
        #Sniper.setLogLevel(level)
        #super().setLogLevel(level)

    def data_keys(self):
        cmd = self.remote_name + ".data_keys()"
        msg_id  = self.kc.execute(cmd)
        exe_msg = self.execute_status(msg_id)
        dat_keys = []
        if 'data' in exe_msg:
            msg   = exe_msg['data']
            msg   = msg[msg.find("[")+1:msg.rfind("]")]
            items = msg.split(',')
            
            #items = exe_msg['data'].split('\n')
            for i in items:
                begin =  i.find("'")
                end   = i.rfind("'")
                dat_keys.append(i[begin+1:end])

        self.dat_keys = dat_keys
        return self.dat_keys

    def algorithm_keys(self):
        cmd = self.remote_name + ".algorithm_keys()"
        msg_id  = self.kc.execute(cmd)
        exe_msg = self.execute_status(msg_id)
        alg_keys = []
        if 'data' in exe_msg:
            msg   = exe_msg['data']
            msg   = msg[msg.find("[")+1:msg.rfind("]")]
            items = msg.split(',')
            
            for i in items:
                begin = i.find("'")
                end   = i.rfind("'")
                alg_keys.append(i[begin+1:end])

        self.alg_keys = alg_keys
        return self.alg_keys

    def get_data(self, data_name):
        raise Exception('Cannot get DataObject from Server')
        #return self.engine.datastore[data_name]


    def get_algorithm(self, algorithm_name):
        if algorithm_name in self.alg_clients.keys():
            return self.alg_clients[algorithm_name]

        cmd = self.remote_name
        if algorithm_name in self.alg_keys:
            cmd = cmd + ".get_algorithm('"+algorithm_name+"')"
        elif algorithm_name in self.algorithm_keys():
            cmd = cmd + ".get_algorithm('"+algorithm_name+"')"
        else:
            return False
        msg_id  = self.kc.execute(cmd)
        exe_msg = self.execute_status(msg_id)
        self.alg_clients[algorithm_name] = DaisyAlgorithm_client(self.kc, exe_msg['code'])
        print(exe_msg['data'])
        
        return self.alg_clients[algorithm_name]

    def execute(self):
        pass
        #raise Exception('Must')

    def finalize(self):
        cmd = self.remote_name
        cmd = cmd + ".finalize()"
        self.kc.execute_interactive(cmd)
        #exe_msg = self.execute_status(msg_id)
        #print(exe_msg)
        #self.engine.finalize()


    def execute_status(self, msg_id):
        code_flag = False
        data_flag = False
        exe_msg = {'msg_id':msg_id}
        while True:
            try:
                kc_msg = self.kc.get_iopub_msg(timeout=5)
                if 'parent_header' in kc_msg and kc_msg['parent_header']['msg_id'] != exe_msg['msg_id']:
                    continue
                #_output_hook_default(kc_msg)    
                msg_type = kc_msg['header']['msg_type']
                msg_cont = kc_msg['content']
                if msg_type == 'stream':
                    exe_msg[msg_cont['name']] = msg_cont['text']
                elif msg_type == 'error':
                    exe_msg['error'] = msg_cont['traceback']
                    print(msg_cont['traceback'])
                    break
                elif msg_type in ('display_data', 'execute_result'):
                    if 'data' in msg_cont:
                        data_flag = True
                        exe_msg['data'] = msg_cont['data'].get('text/plain','')       
                if 'code' in msg_cont:
                    code_flag = True
                    exe_msg['code'] = msg_cont['code']
    
                if code_flag and data_flag:    
                    break        
            except:
                print('timeout kc.get_iopub_msg')
                break      
        return exe_msg
