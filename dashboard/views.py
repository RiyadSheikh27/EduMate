from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.views import generic


# Creating views for home and notes
def home(request):
    return render(request, "dashboard/home.html")


def notes(request):
    return render(request, "dashboard/notes.html")


# Taking Inputs and Displaying Notes
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user,
                title=request.POST["title"],
                description=request.POST["description"],
            )
            notes.save()
        messages.success(
            request, f"Notes Added from {request.user.username} Successfully"
        )
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {"notes": notes, "form": form}
    return render(request, "dashboard/notes.html", context)


# Deleting Notes
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


# Displaing Notes in Details
class NotesDetailView(generic.DetailView):
    model = Notes


# Creating views for home and notes
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST["subject"],
                title=request.POST["title"],
                description=request.POST["description"],
                due=request.POST["due"],
                is_finished=finished,
            )
            homeworks.save()
            messages.success(request, f"Homework Added from {request.user.username}!!")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {"homeworks": homework, "homeworks_done": homework_done, "form": form}
    return render(request, "dashboard/homework.html", context)


# Updating Homework through checkbox
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")
