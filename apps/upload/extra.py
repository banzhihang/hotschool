import os

from qiniu import Auth
from qiniu import BucketManager

from HotSchool.settings import QINIU_AK, QINIU_SK, QINIU_BUCKET_NAME


class QiNiuFileManage:
    """七牛云资源管理"""

    def __init__(self,key:str):
        self.access_key = QINIU_AK
        self.secret_key = QINIU_SK
        self.bucket_name = QINIU_BUCKET_NAME
        self.file_name = os.path.basename(key) # 要操作的文件名
        self.q = Auth(self.access_key, self.secret_key) # 初始化Auth状态
        self.bucket = BucketManager(self.q) # 初始化BucketManager

    def delete(self):
        # 删除
        res,info = self.bucket.delete(self.bucket_name,self.file_name)
        return res,info






