from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
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
            'participants': forms.CheckboxSelectMultiple(),
            'held_at': DateTimePickerInput(format='%Y-%m-%d %H:%M',
                                           options={
                                               "sideBySide": False,
                                               "stepping": 15
                                           })
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
        widgets = {
            'held_at': DateTimePickerInput(format='%Y-%m-%d %H:%M',
                                           options={
                                               "sideBySide": False,
                                               "stepping": 15
                                           })
        }


class LessonDetailsForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Lesson notes'}
        ),
        max_length=4000, required=False)
    clients_attending = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                       queryset=None, required=False)
    clients_not_attending = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                           queryset=None, required=False)

    class Meta:
        model = Lesson
        fields = ('clients_attending', 'clients_not_attending', 'notes')
        widgets = {
            'clients_attending': forms.CheckboxSelectMultiple,
            'clients_not_attending': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(LessonDetailsForm, self).__init__(*args, **kwargs)
        lesson = self.instance
        clients_attending = lesson.participants.all().order_by('name')
        clients_attending_pk = list(clients_attending.values_list('pk', flat=True))
        clients_not_attending = Client.objects.exclude(pk__in=clients_attending_pk).order_by('name')
        clients_not_attending_pk = list(clients_not_attending.values_list('pk', flat=True))
        self.fields['clients_attending'].queryset = clients_attending
        self.fields['clients_not_attending'].queryset = Client.objects.filter(pk__in=clients_not_attending_pk)
        self.initial['clients_attending'] = clients_attending_pk
        self.initial['clients_not_attending'] = []


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
        fields = ('lessons_attended', 'lessons_not_attended',)
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
        widgets = {
            'joined_on': DatePickerInput(format='%Y-%m-%d')
        }


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
        widgets = {
            'purchased_on': DatePickerInput(format='%Y-%m-%d')
        }


class EditCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('type', 'purchased_on', 'begins_on', 'num_lessons', 'expires')
        widgets = {
            'purchased_on': DatePickerInput(format='%Y-%m-%d'),
            'begins_on': DateTimePickerInput(format='%Y-%m-%d'),
            'expires': DateTimePickerInput(format='%Y-%m-%d'),
        }
