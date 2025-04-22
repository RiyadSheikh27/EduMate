from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Creating views for home and notes section
def home(request):
    return render(request, "dashboard/home.html")


@login_required
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
@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


# Displaing Notes in Details
class NotesDetailView(generic.DetailView):
    model = Notes


# Creating views for Homework section
@login_required
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
@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")


# Deleting Homework
@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect(homework)


# Creating views for Youtube section
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()["result"]:
            result_dict = {
                "input": text,
                "title": i["title"],
                "duration": i["duration"],
                "thumbnail": i["thumbnails"][0]["url"],
                "channel": i["channel"]["name"],
                "link": i["link"],
                "views": i["viewCount"]["short"],
                "published": i["publishedTime"],
            }
            desc = ""
            if i.get("descriptionSnippet"):  # corrected key name too
                for j in i["descriptionSnippet"]:
                    desc += j["text"]
            result_dict["description"] = desc
            result_list.append(result_dict)

        context = {"form": form, "results": result_list}
        return render(request, "dashboard/youtube.html", context)
    else:
        form = DashboardForm()
    context = {"form": form}
    return render(request, "dashboard/youtube.html", context)


# Creating views for To-Do section
@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finshed = request.POST["is_finished"]
                if finished == "on":
                    finished == True
                else:
                    finshed = False
            except:
                finished = False
            todos = Todo(
                user=request.user, title=request.POST["title"], is_finished=finished
            )
            todos.save()
            messages.success(request, f"Todo Added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {"form": form, "todos": todo, "todos_done": todos_done}
    return render(request, "dashboard/todo.html", context)


# Updating To-Do through checkbox
@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")


# Deleting To-Do
@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


## Creating views for Books section
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()

        result_list = []
        for i in range(10):
            item = answer["items"][i]["volumeInfo"]
            result_dict = {
                "title": item.get("title"),
                "subtitle": item.get("subtitle"),
                "description": item.get("description"),
                "count": item.get("pageCount"),
                "categories": item.get("categories"),
                "rating": item.get("averageRating"),
                "thumbnail": item.get("imageLinks", {}).get("thumbnail"),
                "preview": item.get("previewLink"),
            }
            result_list.append(result_dict)

        context = {"form": form, "results": result_list}
        return render(request, "dashboard/books.html", context)
    else:
        form = DashboardForm()
        context = {"form": form}
        return render(request, "dashboard/books.html", context)


# Creating views for Homework section
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)

        try:
            answer = r.json()

            phonetics = answer[0]["phonetics"][0].get("text", "")
            audio = answer[0]["phonetics"][0].get("audio", "")
            meaning = answer[0]["meanings"][0]["definitions"][0]
            definition = meaning.get("definition", "")
            example = meaning.get("example", "")
            synonyms = answer[0]["meanings"][0]["definitions"][0].get("synonyms", [])

            context = {
                "form": form,
                "input": text,
                "phonetics": phonetics,
                "audio": audio,
                "definition": definition,
                "example": example,
                "synonyms": synonyms,
            }
        except Exception as e:
            print("Error:", e)
            context = {
                "form": form,
                "input": "",
                "error": "Could not fetch data. Please try again.",
            }

        return render(request, "dashboard/dictionary.html", context)
    else:
        form = DashboardForm()
        context = {"form": form}
        return render(request, "dashboard/dictionary.html", context)


# Creating views for Wikipedia section
def wiki(request):
    if request.method == "POST":
        text = request.POST["text"]
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            "form": form,
            "title": search.title,
            "link": search.url,
            "details": search.summary,
        }
        return render(request, "dashboard/wiki.html", context)
    else:
        form = DashboardForm()
        context = {"form": form}
    return render(request, "dashboard/wiki.html", context)


# Creating views for Conversion section
def conversion(request):
    context = {}
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if "select" in request.POST and form.is_valid():
            measurement_type = form.cleaned_data["measurement"]
            if measurement_type == "length":
                measurement_form = ConversionLengthForm()
            else:
                measurement_form = ConversionMassForm()
            context = {"form": form, "m_form": measurement_form, "input": True}

        elif "convert" in request.POST:
            measurement_type = request.POST.get("measurement")
            form = ConversionForm(initial={"measurement": measurement_type})
            answer = ""

            if measurement_type == "length":
                measurement_form = ConversionLengthForm(request.POST)
                if measurement_form.is_valid():
                    first = measurement_form.cleaned_data["measure1"]
                    second = measurement_form.cleaned_data["measure2"]
                    input_val = measurement_form.cleaned_data["input"]
                    if input_val and float(input_val) >= 0:
                        input_val = float(input_val)
                        if first == "yard" and second == "foot":
                            answer = f"{input_val} yard = {input_val * 3} foot"
                        elif first == "foot" and second == "yard":
                            answer = f"{input_val} foot = {input_val / 3} yard"
                        else:
                            answer = "Same unit conversion."
            else:
                measurement_form = ConversionMassForm(request.POST)
                if measurement_form.is_valid():
                    first = measurement_form.cleaned_data["measure1"]
                    second = measurement_form.cleaned_data["measure2"]
                    input_val = measurement_form.cleaned_data["input"]
                    if input_val and float(input_val) >= 0:
                        input_val = float(input_val)
                        if first == "pound" and second == "kilogram":
                            answer = (
                                f"{input_val} pound = {input_val * 0.453592} kilogram"
                            )
                        elif first == "kilogram" and second == "pound":
                            answer = (
                                f"{input_val} kilogram = {input_val / 0.453592} pound"
                            )
                        else:
                            answer = "Same unit conversion."

            context = {
                "form": form,
                "m_form": measurement_form,
                "input": True,
                "answer": answer,
            }

    else:
        form = ConversionForm()
        context = {"form": form, "input": False}

    return render(request, "dashboard/conversion.html", context)


# Creating views for User Registration
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "dashboard/register.html", context)


# Creating views for Profile
@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)

    homework_done = len(homeworks) == 0
    todos_done = len(todos) == 0

    context = {
        "homeworks": homeworks,
        "todos": todos,
        "homework_done": homework_done,
        "todos_done": todos_done,
    }
    return render(request, "dashboard/profile.html", context)


# Creating views for Logout
def logout_view(request):
    logout(request)
    return redirect("home")
