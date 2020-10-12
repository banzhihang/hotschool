import json
import re
import time
import uuid
from io import BytesIO
import requests

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import Response
import redis

from HotSchool.settings import POOL
from question.models import Answer, Question
from user.models import User, UserDynamic


def uuid_string():
    # 产生uuid字符串，当作图片的名字
    str_timestamp = time.time()
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, str_timestamp)).replace('-','') # 去掉破折号


def modify_headimage_name(request):
    # 修改图片的名字，解决了不能上传含有中文名的图片的问题.使用正则表达式匹配图片的content_type,获得图片的格式
    # 使用随机字符串代替原始图片名
    try:
        img_type = request.data.get('head_portrait').content_type
    except:
        return request
    else:
        pattern = re.compile('[^/]+$')
        tail = re.findall(pattern, img_type)
        path = uuid_string() + '.' + tail[0]
        request.data.get('head_portrait').name = path
        return request


class OpenIdAndImage:
    """获取openid"""

    def __init__(self, code):
        self.openid_url = 'https://api.weixin.qq.com/sns/jscode2session'
        self.app_id = 'wx35df04e950c9cad8'
        self.app_secret = '7107762d645e15f6f49bdfb0e4180aa4'
        self.code = code

    def get_openid(self):
        openid_url = self.openid_url + "?appid=" + self.app_id + "&secret=" + self.app_secret + \
                     "&js_code=" + self.code + "&grant_type=authorization_code"
        res1 = requests.get(openid_url)
        try:
            openid = res1.json()['openid']
        except:
            return Response({"msg": "登录失败"})
        else:
            return openid


def create_user_dynamic(user_id):
    """
    :param user: 动态所属用户
    :param answer:动态所属回答
    :param question:动态所属问题
    """
    user_id = int(user_id)
    coon = redis.Redis(connection_pool=POOL)
    is_exist = coon.exists('dynamic:' + str(user_id))
    if is_exist:
        # 去redis 查询这个人的动态，若有，则先同步此人的动态到数据库,再从数据库查询此人的全部动态
        user_dynamic_list = coon.zrange('dynamic:' + str(user_id), start=0, end=-1, withscores=True)
        if user_dynamic_list:
            coon.delete('dynamic:' + str(user_id))
            # 查询有没有这个人
            try:
                user = User.objects.get(pk=user_id)
            except Exception:
                return Response({'error': '没有此人'})
            else:
                dynamics = []
                for i in user_dynamic_list:
                    # 反序列化用户动态的json数据 不含时间戳
                    dynamic = json.loads(i[0])
                    answer_id = dynamic.get('answer')
                    question_id = dynamic.get('question')
                    # 判断该动态是问题相关还是回答相关
                    if answer_id:
                        answer = Answer.objects.filter(pk=answer_id)
                        # 若不存在该id 则抛弃这条动态
                        if answer.exists():
                            dynamic['answer_id'] = int(answer_id)
                            dynamic.pop('answer')
                        else:
                            continue
                    if question_id:
                        question = Question.objects.filter(pk=question_id)
                        if question.exists():
                            dynamic['question_id'] = int(question_id)
                            dynamic.pop('question')
                        else:
                            continue
                    # 将时间戳添加到dynamic字典，创建dynamic对象，最后批量插入数据库
                    dynamic['add_time'] = float(i[1])
                    dynamic['user'] = user
                    j = UserDynamic(**dynamic)
                    dynamics.append(j)
            # 批量插入
            UserDynamic.objects.bulk_create(dynamics)
