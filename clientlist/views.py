from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.utils.text import slugify
from datetime import timedelta, datetime

# Create your views here.
from .models import Client, Lesson
from .forms import NewLessonForm, \
    LessonDetailsForm, \
    EditLessonForm, \
    ClientNotesForm, \
    NewClientForm, \
    EditClientForm, \
    AddCardForm


def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


def client_details(request, client_slug):
    client = get_object_or_404(Client, slug=client_slug)

    #  TODO: Add decorations to html for expired or empty card and no card
    if request.method == 'POST':
        form = ClientNotesForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            return redirect('client_details', client_slug=client.slug)
    else:
        form = ClientNotesForm(instance=client)
    return render(request, 'client_details.html', {'client': client,
                                                   'form': form})


def edit_client(request, client_slug):
    #  TODO: Write tests for edit_client view
    client = get_object_or_404(Client, slug=client_slug)
    if request.method == 'POST':
        form = EditClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            return redirect('client_details', client_slug=client.slug)
    else:
        form = EditClientForm(instance=client)
    return render(request, 'edit_client.html', {'form': form, 'client': client})


def add_card(request, client_slug):
    client = get_object_or_404(Client, slug=client_slug)
    if request.method == 'POST':
        form = AddCardForm(request.POST)
        if form.is_valid():
            card = form.save()
            client.card = card
            client.save()
            return redirect('client_details', client_slug=client.slug)
    else:
        form = AddCardForm()
    return render(request, 'add_card.html', {'form': form, 'client': client})


def new_client(request):
    if request.method == 'POST':
        form = NewClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.slug = slugify(client.name)  # TODO: Make this a unique slug. Possibly override save function
            client.added_on = datetime.now()
            client.card = None
            client.save()
            return redirect('client_details', client_slug=client.slug)
    else:
        form = NewClientForm()
    return render(request, 'new_client.html', {'form': form})


def lesson_list(request):
    lessons = Lesson.objects.all()
    lessons = lessons.annotate(participant_count=Count('participants'))
    return render(request, 'lesson_list.html', {'lessons': lessons})


def lesson_details(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonDetailsForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save()
            return redirect('lesson_details', pk=lesson.pk)
    else:
        form = LessonDetailsForm(instance=lesson)
    return render(request, 'lesson_details.html', {'lesson': lesson, 'form': form})


def new_lesson(request):
    if request.method == 'POST':
        form = NewLessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewLessonForm()
    return render(request, 'new_lesson.html', {'form': form})


def edit_lesson(request, pk):
    #  TODO: Write tests for edit_client view
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = EditLessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save()
            return redirect('lesson_details', pk=lesson.pk)
    else:
        form = EditLessonForm(instance=lesson)
    return render(request, 'edit_lesson.html', {'form': form, 'lesson': lesson})

