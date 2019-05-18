from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import PilatesClient, Lesson
from .forms import NewLessonForm


def client_list(request):
    clients = PilatesClient.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


def client_details(request, client_slug):
    client = get_object_or_404(PilatesClient, slug=client_slug)
    return render(request, 'client_details.html', {'client': client})


def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'lesson_list.html', {'lessons': lessons})


def lesson_details(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'lesson_details.html', {'lesson': lesson})


def new_lesson(request):
    if request.method == 'POST':
        form = NewLessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewLessonForm()
    return render(request, 'new_lesson.html', {'form': form})
