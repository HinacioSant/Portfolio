from django.shortcuts import render

# Create your views here.

def tdv(request):
    return render(request, "TDV/tdv.html")
