from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import gallery



# Create your views here.

def tg2a(request):
    form = ImageForm()
    gallery_content = gallery.objects.only("image")



    context = {
        "gallery_content": gallery_content,
        'form': form,

    }
    return render(request, "TG2A/tg2a.html", context)


def add_image(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            add = gallery(user= request.user, title=request.POST['title'], image=request.FILES['image'])
            add.save()

            return redirect("add_image")


    return render(request, "TG2A/add_image.html", {'form': form})


def image_page(request, img_id):
    context = {
        "image": gallery.objects.get(id = img_id)
    }
    return render(request, "TG2A/image_page.html", context)
