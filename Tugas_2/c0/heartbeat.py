import Pyro4
import time
import threading

class Heartbeat(object):
    def __init__(self, id):
        self.counter = 0
        self.last_received = time.time()
        self.id = id
        self.connected_device_summary = {}
        self.connected_device = []
        self.connected_device_thread_job = []

    @Pyro4.expose
    def ok(self):
        return "ok"

    @Pyro4.expose
    def ping_interval(self):
        return 3

    @Pyro4.expose
    def new_thread_job(self, id):
        t = threading.Thread(target=self.__new_thread_job, args=(id,))
        t.start()
        self.connected_device.append(id)
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
        server.add_heartbeat_summary(id)
        while True:
            try:
                res = server.signal_heartbeat_all_to_all(id)
                # print(res)
            except (Pyro4.errors.ConnectionClosedError, Pyro4.errors.CommunicationError) as e:
                print(str(e))
                break
            time.sleep(self.ping_interval())

    @Pyro4.expose
    def add_heartbeat_summary(self, id):
        self.connected_device_summary.update({
            id: {
                'counter' : 0,
                'last_received' : time.time()
            }
        })

    @Pyro4.expose
    def signal_heartbeat(self):
        self.counter = self.counter + 1
        self.last_received = time.time()
        return '> message from {} : counter {}, last received {}'.format(self.id, self.counter, self.last_received)

    @Pyro4.expose
    def signal_heartbeat_all_to_all(self, id):
        summary = self.connected_device_summary.get(id)
        new_summary = {
            id: {
                'counter' : summary.get('counter') + 1,
                'last_received' : time.time()
            }
        }
        self.connected_device_summary.update(new_summary)
        self.counter = self.counter + 1
        self.last_received = time.time()
        return '> message from {} : {}'.format(id, new_summary.get(id))
