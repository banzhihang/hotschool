from rest_framework.response import Response
from rest_framework.views import APIView
from qiniu import Auth

from HotSchool.settings import QINIU_AK, QINIU_SK, QINIU_BUCKET_NAME
from puclic import Authtication


class UploadTokenView(APIView):
    """上传凭证视图"""
    authentication_classes = [Authtication, ]

    def get(self,request):
        # 需要填写你的 Access Key 和 Secret Key
        access_key = QINIU_AK
        secret_key = QINIU_SK
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = QINIU_BUCKET_NAME
        # 生成上传 Token，可以指定过期时间等
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name, 3600)
        return Response({'uptoken':token})
