import Pyro4
import sys

namainstance = sys.argv[1] or "fileserver"

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(namainstance)
    fserver = Pyro4.Proxy(uri)
    fserver.pyro_connect()
    return fserver

if __name__ == '__main__':

    s = get_fileserver_object()

    while True:
        str = input(">> ").split(" ")
        if str[0] == "list":
            print(s.list())
        elif str[0] == "create":
            print(s.create(str[1]))
        elif str[0] == "read":
            print(s.read(str[1]))
        elif str[0] == "delete":
            print(s.delete(str[1]))
        elif str[0] == "update":
            print(s.update(str[1], str[2]))
        elif (str[0] == 'exit'):
            exit()
        else:
            print("Please check your input")