from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('bio', views.bio_page, name='bio_page'),
    path('cv', views.cv_page, name='cv_page'),
    path('cv/experience/new/', views.experience_new, name='experience_new'),
    path('cv/experience/<int:pk>/edit', views.experience_edit, name='experience_edit'),
    path('cv/skill/new/', views.skill_new, name='skill_new'),
    path('cv/project/new/', views.project_new, name='project_new'),
    path('cv/project/<int:pk>/edit', views.project_edit, name='project_edit'),
    path('cv/involvement/new/', views.involvement_new, name='involvement_new'),
    path('cv/involvement/<int:pk>/edit', views.involvement_edit, name='involvement_edit'),
]