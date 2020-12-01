import zipfile
from django.conf import settings
import os
class MyZip:
    def __init__(self,zip_file,end_dir):
        self.zip_file = zip_file
        self.end_dir = end_dir

    def parsezip(self):
        self.unzip()
        # list_excel = []
        # for excel in os.listdir(self.end_dir):
        #     # 获取每个 excel的 路径 传送 excel 进行合并表格
        #     print(self.end_dir+'/'+excel)
        return os.listdir(self.end_dir)
    def unzip(self):
        zip_file = zipfile.ZipFile(self.zip_file)
        zip_file.extractall(self.end_dir)
        return os.listdir(self.end_dir)

