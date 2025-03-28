from django.shortcuts import render

def home(request):
    return render(request,'dashboard/home.html')

def notes(request):
    return render(request,'dashboard/notes.html')