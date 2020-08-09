from io import StringIO

from django.contrib import messages
from django.shortcuts import render


def home(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        service_type = request.POST["service"]

        csv_file = request.FILES["fileCSV"]

        if not csv_file.name.endswith(".csv"):
            messages.error(request, "THIS IS NOT A CSV FILE")

        data_set = csv_file.read().decode("UTF-8")
        io_string = StringIO(data_set)
        next(io_string)

    return render(request, "index.html")
