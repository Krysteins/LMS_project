from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, "main_site.html")


def one(request):
    return render(request, "__base__.html")


def two(request):
    return render(request, "base.html")


def three(request):
    return render(request, "navbar.html")
