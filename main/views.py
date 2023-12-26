from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    return render(request, 'main/index.html')


def about(request: HttpRequest):
    return HttpResponse('About page')
