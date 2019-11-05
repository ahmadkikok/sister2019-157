import os
import time
import Pyro4
import Pyro4.errors
import threading

class CRUDList(object):

    def __init__(self):
        self.connected_device = []
        self.connected_device_thread_job = []

    @Pyro4.expose
    def connected_device_list(self):
        return 'connected device : '+', '.join(self.connected_device)

    @Pyro4.expose
    def connected_device_ls(self):
        return ','.join(self.connected_device)

    @Pyro4.expose
    def connected_device_add(self, id):
        print('register '+ id)
        self.connected_device.append(id)

    @Pyro4.expose
    def connected_device_delete(self, id):
        print('unregister '+ id)
        self.connected_device.remove(id)

    @Pyro4.expose
    def command_not_found(self):
        return "command not found"

    @Pyro4.expose
    def command_success(self):
        return "operation success"

    @Pyro4.expose
    def bye(self):
        return "bye!"

    @Pyro4.expose
    def ok(self):
        return "ok"

    @Pyro4.expose
    def fail(self):
        return "fail"

    @Pyro4.expose
    def ping_interval(self):
        return 3

    @Pyro4.expose
    def max_retries(self):
        return 2

    @Pyro4.expose
    def new_thread_job(self, id):
        t = threading.Thread(target=self.__new_thread_job, args=(id,))
        t.start()
        self.connected_device_thread_job.append(t)
        return self.ok()

    def __connect_heartbeat_server(self, id):
        time.sleep(self.ping_interval())
        try:
            uri = "PYRONAME:{}@localhost:7777".format(id)
            server = Pyro4.Proxy(uri)
        except:
            return None
        return server

    def __new_thread_job(self, id):
        server = self.__connect_heartbeat_server(id)
        while True:
            try:
                res = server.signal_heartbeat()
                print(res)
            except (Pyro4.errors.ConnectionClosedError, Pyro4.errors.CommunicationError) as e:
                print(str(e))
                break
            time.sleep(self.ping_interval())

    @Pyro4.expose
    def create(self,filename="",value=""):
        path = os.getcwd()
        name = filename
        filename = os.path.join(path, filename)
        with open(filename, "w+") as f:
            f.write(value)
        return "[ {} ]\n{}".format(name,value)

    @Pyro4.expose
    def update(self,filename="",value=""):
        path = os.getcwd()
        name = filename
        filename = os.path.join(path, filename)
        if(os.path.exists(filename)):
            with open(filename, "w+") as f:
                f.write(value)
            return "[ {} ]\n{}".format(name,value)
        else:
            return "File not found"

    @Pyro4.expose
    def read(self,filename=""):
        path = os.getcwd()
        name = filename
        filename = os.path.join(path, filename)
        if(os.path.exists(filename)):
            with open(filename) as r:
                return "[ {} ]\n{}".format(name, r.read())
        else:
            return "File not found"

    @Pyro4.expose
    def delete(self,filename=""):
        path = os.getcwd()
        filename = os.path.join(path, filename)
        if(os.path.exists(filename)):
            os.remove(filename)
            return("Success")
        else:
            return "File not found"

    @Pyro4.expose
    def list(self):
        path = os.getcwd()
        files = []
        for root, dirs, files in os.walk(path):
            return files

if __name__ == '__main__':
    k = CRUDList()