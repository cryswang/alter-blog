from django.contrib import admin
from .models import Post, Experience, Skill, Project, Involvement

admin.site.register(Post)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Involvement)