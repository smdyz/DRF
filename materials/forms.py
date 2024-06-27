from django import forms

from .models import Lesson


class UpdateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('name', 'description',)
