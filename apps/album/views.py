from django.shortcuts import render, HttpResponse, redirect
from .models import Photo


def home(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'album/list.html', context)


def upload(request):
    if request.method == 'POST' and request.user.is_superuser:
        if request.POST["foreignUrl"]:
            photo = Photo(foreignUrl=request.POST["foreignUrl"])
            photo.save()
            return redirect('album:home')
        images = request.FILES.getlist('images')
        for i in images:
            photo = Photo(image=i)
            photo.save()
    return redirect('album:home')
