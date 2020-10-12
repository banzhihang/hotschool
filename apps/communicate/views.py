from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from puclic import Authtication
from user.models import User


def room(request):
    return render(request, 'chat/room.html')

def room2(request):
    return render(request, 'chat/room2.html')


class HeadAndNickName(APIView):
    """获得用户的昵称和头像"""
    authentication_classes = [Authtication, ]
    def post(self,request):
        from_user = request.data.get('from_user')
        message = request.data.get('message')
        time = request.data.get('time')
        if not from_user:
            return Response('发生错误')
        user = User.objects.filter(pk=int(from_user)).values_list('nick_name','head_portrait')
        nick_name,head_portrait = user[0][0],user[0][1]

        return Response({'nick_name':nick_name,'head_portrait':head_portrait,'from_user':from_user,
                         'message':message,'time':time})