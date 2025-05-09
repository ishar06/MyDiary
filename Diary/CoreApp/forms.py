from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DiaryEntry

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'mood', 'font_size', 'font_style',
                 'is_bold', 'is_italic', 'is_underline', 'is_strikethrough']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'font_size': forms.Select(attrs={'class': 'form-control'}),
            'font_style': forms.Select(attrs={'class': 'form-control'}),
            'is_bold': forms.HiddenInput(),
            'is_italic': forms.HiddenInput(),
            'is_underline': forms.HiddenInput(),
            'is_strikethrough': forms.HiddenInput(),
        }