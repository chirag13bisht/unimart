from django.shortcuts import render

def home(request):
    return render(request, "home.html")


def waitlist(request):
    return render(request, "waitlist.html")

