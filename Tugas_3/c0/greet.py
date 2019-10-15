import os

class CRUDList(object):

    def __init__(self):
        pass

    def create(self,filename="",value=""):
        path = os.getcwd()
        name = filename
        filename = os.path.join(path, filename)
        with open(filename, "w+") as f:
            f.write(value)
        return "[ {} ]\n{}".format(name,value)

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

    def read(self,filename=""):
        path = os.getcwd()
        name = filename
        filename = os.path.join(path, filename)
        if(os.path.exists(filename)):
            with open(filename) as r:
                return "[ {} ]\n{}".format(name, r.read())
        else:
            return "File not found"

    def delete(self,filename=""):
        path = os.getcwd()
        filename = os.path.join(path, filename)
        if(os.path.exists(filename)):
            os.remove(filename)
            return("Success")
        else:
            return "File not found"

    def list(self):
        path = os.getcwd()
        files = []
        for root, dirs, files in os.walk(path):
            return files

if __name__ == '__main__':
    k = CRUDList()