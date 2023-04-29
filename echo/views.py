from django.shortcuts import render, HttpResponse
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, 'echo/index.html')
