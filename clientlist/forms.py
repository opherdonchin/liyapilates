from django import forms
from .models import Lesson

class NewLessonForm(forms.ModelForm):
    # TODO: Description field should not be required.
    # TODO: Date for new lesson should default to today.
    # TODO: Date format for new lesson should be right
    # TODO: Add selector widget for Date and time
    # TODO: Client selection by checkboxes for new lesson

    class Meta:
        model = Lesson
        fields = {'held_at', 'session_type', 'description', 'participants'}