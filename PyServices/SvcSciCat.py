from __future__ import print_function

import Daisy
class SvcSciCat(Daisy.Base.DaisySvc):

    def __init__(self, name):
        super().__init__(name)
        self.access_point = 'http://192.168.14.92:3000/api/v3/'
        self.headers      = {"Content-Type": "application/json;charset=UTF-8"}
        pass

    def initialize(self, username='admin', password='ihep123'):
        self.user_info = {"username":username, "password":password}
        self.LogInfo("initialized SvcSciCat")
        return True

    def __login(self):
        url = self.access_point+"Users/login"
        r = requests.post(url=url, json=self.user_info, headers=self.headers)
        token = (r.json()["id"])
        return (token)

    def __polishPID(self, pid = None):
        if type(pid) is str:
            return pid.replace('/','%2F')
        else:
            return pid

    def execute(self):
        self.LogInfo("execute SvcSciCat, Hello Daisy ")
        return True

    def finalize(self):
        self.LogInfo("finalize SvcSciCat, Hello Daisy ")
        return True






