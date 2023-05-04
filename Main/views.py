from django.shortcuts import render, redirect
from django.views.debug import ExceptionReporter

# Create your views here.



def index(request):
    print(request.META['HTTP_HOST'])
    reporter = ExceptionReporter(request, exc_type, exc_value, traceback)
    html_report = reporter.get_traceback_html()
    text_report = reporter.get_traceback_text()
    print(html_report)
    print(text_report)
    return render(request, "PTs/index.html")

def projects(request):
    return render(request, "PTs/projects.html")

def resume(request):
    return render(request, "PTs/resume.html")

def about(request):
    return render(request, "PTs/about.html")
