from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "PTs/index.html")

def projects(request):
    if not request.user.is_authenticated:
        return redirect("/lg")
        
    return render(request, "PTs/projects.html")

def resume(request):
    return render(request, "PTs/resume.html")

def about(request):
    return render(request, "PTs/about.html")
