import json

from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe


def index(request):
    return render(request, 'chat/index.html', {})

def room(request):
    return render(request, 'chat/room.html')

def room2(request):
    return render(request, 'chat/room2.html')