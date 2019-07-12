from django import forms
from .models import Lesson, Client, Card


class NewLessonForm(forms.ModelForm):
    # TODO: Date format for new lesson should be right
    # TODO: Add selector widget for Date and time
    # TODO: Client selection by checkboxes for new lesson
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Lesson notes'}
        ),
        max_length=4000, required=False)

    class Meta:
        model = Lesson
        fields = ('held_at', 'type', 'notes', 'participants')
        widgets = {
            'participants': forms.CheckboxSelectMultiple
        }


class EditLessonForm(forms.ModelForm):
    # TODO: Date format for new lesson should be right
    # TODO: Add selector widget for Date and time
    # TODO: Client selection by checkboxes for new lesson
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Lesson notes'}
        ),
        max_length=4000, required=False)

    class Meta:
        model = Lesson
        fields = ('held_at', 'type', 'notes')


class LessonDetailsForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Lesson notes'}
        ),
        max_length=4000, required=False)

    class Meta:
        model = Lesson
        fields = ('participants', 'notes')
        widgets = {
            'participants': forms.CheckboxSelectMultiple
        }


class ClientNotesForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Client notes'}
        ),
        max_length=4000, required=False)

    class Meta:
        model = Client
        fields = ('notes',)


class ClientLessonsForm(forms.ModelForm):
    lessons_attended = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                      queryset=None, required=False)
    lessons_not_attended = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                          queryset=None, required=False)

    class Meta:
        model = Client
        fields = ('lessons_attended', 'lessons_not_attended', )
        widgets = {'lessons_attended': forms.CheckboxSelectMultiple,
                   'lessons_not_attended': forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super(ClientLessonsForm, self).__init__(*args, **kwargs)
        client = self.instance
        client_attended = client.lessons.all()
        client_attended_pk = list(client_attended.values_list('pk', flat=True))
        client_not_attended = Lesson.objects.exclude(pk__in=client_attended_pk).order_by('-held_at')[:10]
        client_not_attended_pk = list(client_not_attended.values_list('pk', flat=True))
        self.fields['lessons_attended'].queryset = client_attended
        self.fields['lessons_not_attended'].queryset = Lesson.objects.filter(pk__in=client_not_attended_pk)
        self.initial['lessons_attended'] = client_attended_pk
        self.initial['lessons_not_attended'] = []


class NewClientForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Client notes'}
        ),
        max_length=4000, required=False)

    class Meta:
        model = Client
        fields = ('name', 'joined_on', 'notes')


class EditClientForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Client notes'}
        ),
        max_length=4000)

    class Meta:
        model = Client
        fields = ('name', 'notes')


class AddCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('type', 'purchased_on')


class EditCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('type', 'purchased_on', 'begins_on', 'num_lessons', 'expires')
