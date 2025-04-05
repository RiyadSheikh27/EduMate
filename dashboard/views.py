from django.shortcuts import render
from .models import Notes


# Home view
def home(request):
    return render(request, "dashboard/home.html")


def notes(request):
    return render(request, "dashboard/notes.html")


# Displaying Notes
def notes(request):
    notes = Notes.objects.filter(user=request.user)
    context = {"notes": notes}
    return render(request, "dashboard/notes.html", context)
