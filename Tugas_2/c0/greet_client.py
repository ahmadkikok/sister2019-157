import Pyro4
import os

def get_server():
    uri = "PYRONAME:crud@localhost:7777"
    gserver = Pyro4.Proxy(uri)
    return gserver

if __name__=='__main__':
    server = get_server()
    while True:
        print("1. Use 'mk [filename]' to create new file\n2. Use 'read [filename] to read file\n3. Use 'up [filename]'to update file\n4. Use 'rm [filename]' to delete file\n5. Use 'ls' to show files or directory\n0. Use 'exit' to close program")
        str = input('>> ').split(' ')
        if(str[0] == 'mk'):
            content = input("Content : ")
            print(server.create(str[1], content))
        elif(str[0] == 'read'):
            print(server.read(str[1]))
        elif(str[0] == 'up'):
            content = input("Content : ")
            print(server.update(str[1], content))
        elif(str[0] == 'rm'):
            print(server.delete(str[1]))
        elif(str[0] == 'ls'):
            print('\n'.join(server.list()))
        elif(str[0] == 'exit'):
            exit()
        else:
            print("Please check your input")