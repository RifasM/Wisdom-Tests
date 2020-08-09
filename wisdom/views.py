from django.shortcuts import render


def home(request):
    if request.method == "POST":
        pass

    return render(request, "index.html")
