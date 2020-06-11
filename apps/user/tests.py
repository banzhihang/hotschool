
from django.test import TestCase
import requests
from PIL import Image
from io import BytesIO
import re

from django.core.files.uploadedfile import InMemoryUploadedFile

img_url = 'https://wx.qlogo.cn/mmopen/vi_32/E2L7eCcteRTnqE6klRT4tcTNYUb2arB7iaicQdlHQuHUcryJezXbtptggsxnWZSqg4AernyGEMSic7iaXoVicdkDJyA/132'
res2 = requests.get(img_url)

a=res2.content
tail = res2.headers.get("Content-Type")
pattern = re.compile('[^/]+$')
b=re.findall(pattern,tail)
print(tail)
bytes_stream = BytesIO(a)
image = InMemoryUploadedFile(bytes_stream, None, 'aa'+'.'+b[0], None, len(a), None, None)
print(1)