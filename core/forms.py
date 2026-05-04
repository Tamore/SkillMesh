from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Post, Skill, Message

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'open_to_work']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'open_to_work': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SkillForm(forms.Form):
    skill_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Add a skill (e.g. Python, Django, AWS)'
    }))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'post_type', 'related_skills']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': "What's on your mind?"}),
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'related_skills': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_skills'].queryset = Skill.objects.all()
        self.fields['related_skills'].required = False

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your message...'}),
        }

class CustomUserCreationForm(forms.Form):
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-white border-0 py-3 px-4 rounded-3',
        'placeholder': 'John Doe'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control bg-dark text-white border-0 py-3 px-4 rounded-3',
        'placeholder': 'john@example.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-white border-0 py-3 px-4 rounded-3',
        'placeholder': '••••••••'
    }))
    agree = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input bg-dark border-secondary'
    }))
