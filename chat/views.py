from django.http import HttpResponse
from django.shortcuts import render


def chat_index(request):
    return HttpResponse('Chat page')
