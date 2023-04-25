from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import gallery, favorite, reports
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .gallery_management import image_management, infinite_scroll
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone


# Create your views here.

def tg2a(request):
    a = reports(image_id = "tg2a_pageview", reason = "Guest use", more_info = timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    a.save()

    # Main page
    context = {
        "form": ImageForm(), # Form load for the add image element.
    }

    return render(request, "TG2A/tg2a.html", context)


def add_image(request):
    if not request.user.is_authenticated:
        return redirect("TG2A")
    # Add image

    if request.method == 'POST':
        # Image add class/method. Check gallery_management.py for more info.
        try:
            if request.POST['action'] == "delete_img":
                response = image_management(user=request.user, form=request.POST).delete_img()


        except MultiValueDictKeyError:

            response = image_management(user=request.user, form=ImageForm(request.POST, request.FILES)).add_image()

        if response:

            context = {
                "form": ImageForm(), # Form load for the add image element.
                "error": response,
            }

            return render(request, "TG2A/tg2a.html", context)


    return redirect("TG2A")

def image_page(request, img_id):
    response = ""
    # Image page (specific image page)

    img = gallery.objects.get(id=img_id) # Query for image.

    # Check if the image is mark as favorite for the person on the page. Check gallery_management.py for more info.
    if request.user.is_authenticated:
        response = image_management(user=request.user,form=img).check() # return the the response

    if request.method == "POST":
        # Management of the favorite function. Check gallery_management.py for more info.
        image_management(user=request.user, form= img).fav(fav_form=request.POST['fav'])

    context = {
        "image": img,
        "fav": response,
    }

    return render(request, "TG2A/image_page.html", context)

def gallery_items(request, page_num):

    # Management of the pagination/infinite scroll. Check gallery_management.py for more info.
    response = infinite_scroll(gallery_content = gallery.objects.only("id", "thumbnail_url").order_by('-date'), page = request.GET.get('page', page_num))

    return JsonResponse({"items": response["items"].object_list, "page": response["page_num"]})

def report(request):

    if request.method == "POST":
        form = request.POST
        add = reports(image_id = form['img_id'], reason = form['reason'], more_info = form['m_info'])
        add.save()

    return HttpResponse("200")

def profile(request, user):

    # Query's for the profile page.
    user_1 = User.objects.get(username=user)
    fav = favorite.objects.filter(user=user_1, favorite = True).order_by('-id')
    all_uploads = gallery.objects.filter(user=user_1).order_by('-date')

    if request.user != user_1:
        user_p = False
    else:
        user_p = True

    context = {
        "fav": fav,
        "user_profile": user,
        "all_uploads": all_uploads,
        "user_p": user_p,
    }
    return render(request, "TG2A/profile.html", context)
