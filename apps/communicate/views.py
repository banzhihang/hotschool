from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from HotSchool.settings import domain_name
from user.models import User


def room(request):
    return render(request, 'chat/room.html')

def room2(request):
    return render(request, 'chat/room2.html')

class HeadAndNickName(APIView):
    """获得用户的昵称和头像"""
    def get(self,request):
        user_id = request.GET.get('user')
        user = User.objects.filter(pk=int(user_id)).values_list('nick_name','head_portrait')
        nick_name,head_portrait = user[0][0],domain_name+'/media/'+user[0][1]

        return Response({'nick_name':nick_name,'head_portrait':head_portrait})