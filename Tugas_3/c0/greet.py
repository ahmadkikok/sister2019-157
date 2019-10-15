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
    def connected_device_list(self) -> str:
        return 'connected device : ' + ', '.join(self.connected_device)

    @Pyro4.expose
    def connected_device_ls(self) -> str:
        return ','.join(self.connected_device)

    @Pyro4.expose
    def connected_device_add(self, id):
        print('register ' + id)
        self.connected_device.append(id)

    @Pyro4.expose
    def connected_device_delete(self, id):
        print('unregister ' + id)
        self.connected_device.remove(id)

    @Pyro4.expose
    def command_not_found(self) -> str:
        return "command not found"

    @Pyro4.expose
    def command_success(self) -> str:
        return "operation success"

    @Pyro4.expose
    def bye(self) -> str:
        return "bye!"

    @Pyro4.expose
    def ok(self) -> str:
        return "ok"

    @Pyro4.expose
    def fail(self) -> str:
        return "fail"

    @Pyro4.expose
    def ping_interval(self) -> int:
        return 3

    @Pyro4.expose
    def max_retries(self) -> int:
        return 2

    @Pyro4.expose
    def new_thread_job(self, id) -> str:
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

    def __delete_file(self, path, name) -> str:
        res = self.command_success()
        try:
            os.remove(os.path.join(path, name))
        except Exception as e:
            return str(e)
        return res

    def __process_file(self, path, name, operation, *args, **kwargs) -> str:
        res = self.command_success()
        try:
            f = open(os.path.join(path, name), operation)
            if operation == "r":
                res = f.read()
            elif operation == "a+":
                f.write(kwargs.get('content', None))
            f.close()
        except Exception as e:
            return str(e)
        return res

    def __root_folder_exists(self, root):
        if not os.path.exists(root):
            os.makedirs(root)

    def __get_storage_path(self) -> str:
        root = os.path.dirname(os.path.abspath(__file__)) + "/storage"
        self.__root_folder_exists(root)
        return root

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