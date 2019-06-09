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
        max_length=4000)

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
        max_length=4000)

    class Meta:
        model = Lesson
        fields = ('held_at', 'type', 'notes')


class LessonDetailsForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Lesson notes'}
        ),
        max_length=4000)

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
        max_length=4000)

    class Meta:
        model = Client
        fields = ('notes', )


class NewClientForm(forms.ModelForm):
    # TODO: Description field in new client form (get code from SignUpForm in boards)
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Client notes'}
        ),
        max_length=4000)

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
