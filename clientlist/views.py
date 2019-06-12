from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, OuterRef, Subquery, Q, F
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime

# Create your views here.
from .models import Client, Lesson, Card
from .forms import NewLessonForm, \
    LessonDetailsForm, \
    EditLessonForm, \
    ClientNotesForm, \
    NewClientForm, \
    EditClientForm, \
    AddCardForm


def client_list(request):
    clients = Client.objects.all()

    current_cards = Card.objects.filter(client=OuterRef('slug'),
                                        purchased_on__lte=timezone.now(),
                                        expires__gte=timezone.now()).order_by("-purchased_on")
    newest_lessons = Lesson.objects.filter(participants=OuterRef('slug')).values('participants').order_by('held_at')

    clients = clients.annotate(card_type=Subquery(current_cards[:1].values('type__name'))) \
        .annotate(card_begins_on=Subquery(current_cards[:1].values('begins_on'))) \
        .annotate(card_expires=Subquery(current_cards[:1].values('expires'))) \
        .annotate(card_num_lessons=Subquery(current_cards[:1].values('num_lessons'))) \
        .annotate(card_lessons_used=Count(
        'lessons__pk', filter=Q(lessons__held_at__gte=F('card_begins_on'),
                                lessons__held_at__lte=F('card_expires'),
                                ), distinct=True)) \
        .annotate(card_lessons_left=F('card_num_lessons') - F('card_lessons_used')) \
        .annotate(latest_lesson_date=Subquery(newest_lessons[:1].values('held_at'))) \
        .annotate(latest_lesson_pk=Subquery(newest_lessons[:1].values('pk')))

    return render(request, 'client_list.html', {'clients': clients})


def client_details(request, client_slug):
    client = get_object_or_404(Client, slug=client_slug)
    client.card = client.cards\
        .filter(begins_on__lte=timezone.now(), expires__gte=timezone.now())\
        .latest('-expires')

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
