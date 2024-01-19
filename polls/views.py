from django.http import HttpResponse
from django.shortcuts import render


def polls_index(request):
    return HttpResponse('Polls page')
