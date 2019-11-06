import os
import Pyro4

class FileServer(object):
    def __init__(self):
        self.pyro_server = ["fileserver","fileserver2","fileserver3"]
        self.pyro = dict()

    def pyro_connect(self):
        i = 0
        for list in self.pyro_server:
            uri = "PYRONAME:{}@localhost:7777" . format(list)
            self.pyro[i] = Pyro4.Proxy(uri)
            i+=1

    def create_return_message(self,kode='000',message='kosong',data=None):
        return dict(kode=kode,message=message,data=data)

    def list(self):
        print("list ops")
        try:
            daftarfile = []
            for x in os.listdir():
                if x[0:4]=='FFF-':
                    daftarfile.append(x[4:])
            return self.create_return_message('200',daftarfile)
        except:
            return self.create_return_message('500','Error')

    def create(self, name='filename000'):
        for x in range(0, len(self.pyro)):
            self.pyro[x].create(name)

        nama='FFF-{}' . format(name)
        print("create ops {}" . format(nama))
        try:
            if os.path.exists(name):
                return self.create_return_message('102', 'OK','File Exists')
            f = open(nama,'wb',buffering=0)
            f.close()
            return self.create_return_message('100','OK')
        except:
            return self.create_return_message('500','Error')
    def read(self,name='filename000'):
        nama='FFF-{}' . format(name)
        print("read ops {}" . format(nama))
        try:
            f = open(nama,'r+b')
            contents = f.read().decode()
            f.close()
            return self.create_return_message('101','OK',contents)
        except:
            return self.create_return_message('500','Error')
    def update(self,name='filename000',content=''):
        for x in range(0, len(self.pyro)):
            self.pyro[x].update(name, content)

        nama='FFF-{}' . format(name)
        print("update ops {}" . format(nama))

        if (str(type(content))=="<class 'dict'>"):
            content = content['data']
        try:
            f = open(nama,'w+b')
            f.write(content.encode())
            f.close()
            return self.create_return_message('101','OK')
        except Exception as e:
            return self.create_return_message('500','Error',str(e))

    def delete(self,name='filename000'):
        for x in range(0, len(self.pyro)):
            self.pyro[x].delete(name)

        nama='FFF-{}' . format(name)
        print("delete ops {}" . format(nama))

        try:
            os.remove(nama)
            return self.create_return_message('101','OK')
        except:
            return self.create_return_message('500','Error')

if __name__ == '__main__':
    k = FileServer()