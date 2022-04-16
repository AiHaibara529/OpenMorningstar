from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import main


def index(request):
    node_file = "./apps/v2ray/static/v2ray/node.json"
    secret = main.run(node_file)
    return HttpResponse(secret)
