from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, OuterRef, Subquery, Q, F
from django.views.generic import ListView
from django.utils.text import slugify
from django.utils import timezone
from django.http import Http404
from datetime import datetime

# Create your views here.
from .models import Client, Lesson, Card
from .forms import NewLessonForm, \
    LessonDetailsForm, \
    EditLessonForm, \
    ClientNotesForm, \
    NewClientForm, \
    EditClientForm, \
    AddCardForm, \
    EditCardForm, \
    ClientLessonsForm


# TODO: Add user authentication and make client and admin views

def client_list(request):
    clients = Client.objects.all()

    current_cards = Card.objects.filter(client=OuterRef('pk'),
                                        purchased_on__lte=timezone.now(),
                                        expires__gte=timezone.now()).order_by("purchased_on")
    newest_lessons = Lesson.objects.filter(participants=OuterRef('pk')).values('participants').order_by('held_at')

    clients = clients.annotate(card_type=Subquery(current_cards[:1].values('type__name'))) \
        .order_by('name') \
        .annotate(card_begins_on=Subquery(current_cards[:1].values('begins_on'))) \
        .annotate(card_expires=Subquery(current_cards[:1].values('expires'))) \
        .annotate(card_num_lessons=Subquery(current_cards[:1].values('num_lessons'))) \
        .annotate(card_lessons_used=Count('lessons__pk', filter=Q(lessons__held_at__gte=F('card_begins_on'),
                                                                  lessons__held_at__lte=F('card_expires'),
                                                                  ), distinct=True)) \
        .annotate(card_lessons_left=F('card_num_lessons') - F('card_lessons_used')) \
        .annotate(latest_lesson_date=Subquery(newest_lessons[:1].values('held_at'))) \
        .annotate(latest_lesson_pk=Subquery(newest_lessons[:1].values('pk')))

    return render(request, 'client_list.html', {'clients': clients})


def client_details(request, client_slug):
    client = get_object_or_404(Client, slug=client_slug)
    if client.cards.count() > 0:
        client.card = client.cards \
            .filter(begins_on__lte=timezone.now(), expires__gte=timezone.now()) \
            .latest('-purchased_on')
    else:
        client.card = None

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
            card = form.save(commit=False)
            card.num_lessons = card.type.num_lessons
            card.expires = card.default_expiration()
            card.save()
            client.cards.add(card)
            client.save()
            return redirect('client_details', client_slug=client.slug)
    else:
        form = AddCardForm()
    return render(request, 'add_card.html', {'form': form, 'client': client})


def edit_card(request, client_slug, card_pk):
    client = get_object_or_404(Client, slug=client_slug)
    card = get_object_or_404(Card, pk=card_pk)
    if card not in client.cards.get_queryset():
        raise Http404
    if request.method == 'POST':
        form = EditCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('client_cards', client_slug=client.slug)
    else:
        form = EditCardForm(instance=card)
    return render(request, 'edit_card.html', {'form': form, 'client': client, 'card': card})


class ClientCards(ListView):
    model = Card
    context_object_name = 'cards'
    template_name = 'client_cards.html'
    paginate_by = 5

    def __init__(self):
        super().__init__()
        self.client = None

    def get_context_data(self, **kwargs):
        kwargs['client'] = self.client
        return super().get_context_data(**kwargs)

    def get_queryset(self, **kwargs):
        self.client = get_object_or_404(Client, slug=self.kwargs.get('client_slug'))
        queryset = self.client.cards.order_by('-expires')
        return queryset


def client_lessons(request, client_slug):
    client = get_object_or_404(Client, slug=client_slug)
    if request.method == 'POST':
        form = ClientLessonsForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            lessons_attended = form.cleaned_data['lessons_attended']
            lessons_not_attended = form.cleaned_data['lessons_not_attended']
            client.lessons.clear()
            for lesson in lessons_attended:
                client.lessons.add(lesson)
            for lesson in lessons_not_attended:
                client.lessons.add(lesson)

            client.save()
            return redirect('client_details', client_slug=client_slug)
    else:
        form = ClientLessonsForm(instance=client)
    return render(request, 'client_lessons.html', {'client': client, 'form': form})


def new_client(request):
    if request.method == 'POST':
        form = NewClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)

            translated_name = client.name_in_english() # Convert Hebrew characters to English sound-alikes
            client.slug = slugify(translated_name)  # TODO: Make this a unique slug. Possibly override save function
            client.added_on = datetime.now()
            client.card = None
            client.save()
            return redirect('client_details', client_slug=client.slug)
    else:
        form = NewClientForm()
    return render(request, 'new_client.html', {'form': form})


def lesson_list(request):
    lessons = Lesson.objects.all()
    lessons = lessons.annotate(participant_count=Count('participants')).order_by('-held_at')
    return render(request, 'lesson_list.html', {'lessons': lessons})


# TODO: Refactor lesson_details as FormView class

def lesson_details(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonDetailsForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            clients_attending = form.cleaned_data['clients_attending']
            clients_not_attending = form.cleaned_data['clients_not_attending']
            lesson.participants.clear()
            for client in clients_attending:
                lesson.participants.add(client)
            for client in clients_not_attending:
                lesson.participants.add(client)
            lesson.save()
            return redirect('lesson_details', pk=lesson.pk)
    else:
        form = LessonDetailsForm(instance=lesson)
    return render(request, 'lesson_details.html', {'lesson': lesson, 'form': form})


def new_lesson(request):
    if request.method == 'POST':
        form = NewLessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = NewLessonForm()
    return render(request, 'new_lesson.html', {'form': form})


def edit_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = EditLessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save()
            return redirect('lesson_details', pk=lesson.pk)
    else:
        form = EditLessonForm(instance=lesson)
    return render(request, 'edit_lesson.html', {'form': form, 'lesson': lesson})
