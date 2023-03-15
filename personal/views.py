from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "personal/index.html")


def aboutmail(request):
    return render(request, "personal/aboutmail.html")


def aboutauction(request):
    return render(request, "personal/aboutauction.html")


def aboutnetwork(request):
    return render(request, "personal/aboutnetwork.html")