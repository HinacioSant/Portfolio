from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from . import user_management as um

# Create your views here.

def msaindex(request):
    if request.method == "POST":
        form = request.POST
        request.session['name'] = form['iname']
        response = um.user_g(name=form['iname'], status='False').add()
        if response == 'User already exists':
            print(response)
            return redirect('msa')

        return redirect('msa_menu')

    return render(request, "MSA/msaindex.html")


def msa_menu(request):
    try:
        x = User.objects.get(username=request.session['name'])
    except ObjectDoesNotExist:
        return redirect('msa')

    return render(request, "MSA/msa_menu.html", {'msa_name' : x})
