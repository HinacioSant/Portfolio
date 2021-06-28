from django.shortcuts import render

# Create your views here.
def msaindex(request):
    if request.method == "POST":
        form = request.POST
        request.session['name'] = form['iname']
        print(request.session['name'])
    return render(request, "MSA/msaindex.html")
