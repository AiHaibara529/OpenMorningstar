from django.shortcuts import render, HttpResponse

def index(request):
	count = 2
	return render(request, 'shop/index.html',locals())
