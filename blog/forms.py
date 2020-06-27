from django import forms

from .models import Post, Experience

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ('company', 'title', 'description', 'location', 'work_period',)
