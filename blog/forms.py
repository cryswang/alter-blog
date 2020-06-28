from django import forms
from .models import Post, Experience, Skill, Project, Involvement

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ('company', 'title', 'description', 'location', 'work_period',)

class SkillsForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ('title', 'experienced', 'level',)

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('title', 'description', 'work_period',)

class InvolvementForm(forms.ModelForm):

    class Meta:
        model = Involvement
        fields = ('name', 'role', 'description', 'work_period',)