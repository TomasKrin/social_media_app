from django.http import HttpResponse
from django.shortcuts import render


def home_index(request):
    return HttpResponse('Home/social-media page')
