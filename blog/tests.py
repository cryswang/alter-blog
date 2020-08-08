from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test.client import Client
from blog.views import post_list, bio_page, cv_page, post_detail
from blog.models import Post, Experience, Skill, Project, Involvement
from blog.forms import PostForm, ExperienceForm, SkillsForm, ProjectForm, InvolvementForm

class BlogTest(TestCase):

    def test_root_url_resolves_to_blog(self):
        found = resolve('/')  
        self.assertEqual(found.func, post_list) 
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateUsed(response, 'blog/post_list.html')
    
    def test_new_post_returns_correct_html(self):
        response = self.client.get('/post/new/')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateUsed(response, 'blog/post_edit.html')
    
    def test_blog_edit_returns_correct_html(self):
        response = self.client.get('/post/new/')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateUsed(response, 'blog/post_edit.html')
    
class PostModelTest(TestCase):

    def test_can_save_a_POST_request(self):
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        my_admin = authenticate(username='myuser', password=password)
        self.client.login(username='myuser', password=password)
        response = self.client.post('/post/new/', data={'title':'something', 'text': 'this is text'})
        new_item = Post.objects.first()  
        self.assertEqual(new_item.title, 'something')
        self.assertEqual(new_item.text, 'this is text')

    def test_saving_and_retrieving_posts(self):
        admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'mypassword')
        initialCount = Post.objects.all().count()
        first_item = Post()
        first_item.author = admin
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Post()
        second_item.author = admin
        second_item.text = 'Item the second'
        second_item.save()

        current_items = Post.objects.all()
        self.assertEqual(current_items.count(), initialCount + 2)

        first_saved_item = current_items[0]
        second_saved_item = current_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

    def test_detect_invalid_post_form(self):
        form_data = {'title': 'something'}
        form = PostForm(data=form_data)
        self.assertTrue(not form.is_valid())

        form_data = {'text': 'something'}
        form = PostForm(data=form_data)
        self.assertTrue(not form.is_valid())


class BioPageTest(TestCase):
    def test_bio_url_resolves_to_bio_page(self):
        found = resolve('/bio')  
        self.assertEqual(found.func, bio_page)
    
    def test_bio_page_returns_correct_html(self):
        response = self.client.get('/bio')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateUsed(response, 'blog/bio_page.html')

class CVPageTest(TestCase):    
    def test_cv_url_resolves_to_cv_page(self):
        found = resolve('/cv')  
        self.assertEqual(found.func, cv_page)
    
    def test_cv_page_returns_correct_html(self):
        response = self.client.get('/cv')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateUsed(response, 'blog/cv_page.html')

class ExperienceModelTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        my_admin = authenticate(username='myuser', password=password)
        self.client.login(username='myuser', password=password)

        response = self.client.post('/cv/experience/new/', data={
            'company': 'nerdwallet',
            'title':'intern',
            'description': 'this is what i did',
            'location': 'remote',
            'work_period': 'today'})
        new_item = Experience.objects.first()  
        self.assertEqual(new_item.company, 'nerdwallet')
        self.assertEqual(new_item.title, 'intern')
        self.assertEqual(new_item.description, 'this is what i did')
        self.assertEqual(new_item.location, 'remote')
        self.assertEqual(new_item.work_period, 'today')
    
    def test_saving_and_retrieving_experiences(self):
        initialCount = Experience.objects.all().count()
        first_item = Experience()
        first_item.company = 'The umbrella company'
        first_item.title = 'intern'
        first_item.description = 'rezident evil game'
        first_item.location = 'zombieland'
        first_item.work_period = 'back in the old days'
        first_item.save()

        second_item = Experience()
        second_item.company = 'deer park water'
        second_item.title = 'taste tester'
        second_item.description = 'drank water'
        second_item.location = 'pennsylvania'
        second_item.work_period = '2021'
        second_item.save()

        current_items = Experience.objects.all()
        self.assertEqual(current_items.count(), initialCount + 2)

        first_saved_item = current_items[0]
        second_saved_item = current_items[1]
        self.assertEqual(first_saved_item.company, 'The umbrella company')
        self.assertEqual(second_saved_item.location, 'pennsylvania')

    def test_detect_invalid_exp_form(self):
        form_data = {'company': 'something'}
        form = ExperienceForm(data=form_data)
        self.assertTrue(not form.is_valid())

        form_data = {
            'title': 'intern',
            'description': 'this is what i did',
            'location': 'remote',
            'work_period': 'today'
        }
        form = ExperienceForm(data=form_data)
        self.assertTrue(not form.is_valid())

class SkillModelTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        my_admin = authenticate(username='myuser', password=password)
        self.client.login(username='myuser', password=password)

        response = self.client.post('/cv/skill/new/', data={
            'title': 'wall-climbing',
            'experienced': True,
            'level': 0})
        new_item = Skill.objects.first()  
        self.assertEqual(new_item.title, 'wall-climbing')
        self.assertTrue(new_item.experienced)
        self.assertEqual(new_item.level, 0)
    
    def test_saving_and_retrieving_skills(self):
        initialCount = Skill.objects.all().count()
        first_item = Skill()
        first_item.title = 'interning'
        first_item.experienced = True
        first_item.level = 1
        first_item.save()

        second_item = Skill()
        second_item.title = 'testing'
        second_item.experienced = False
        second_item.level = 3
        second_item.save()

        current_items = Skill.objects.all()
        self.assertEqual(current_items.count(), initialCount + 2)

        first_saved_item = current_items[0]
        second_saved_item = current_items[1]
        self.assertEqual(first_saved_item.title, 'interning')
        self.assertEqual(second_saved_item.title, 'testing')
        self.assertTrue(first_saved_item.experienced)
        self.assertTrue(first_saved_item.level, 1)
        self.assertFalse(second_saved_item.experienced)
        self.assertEqual(second_saved_item.level, 3)

    def test_detect_invalid_exp_form(self):
        form_data = {'title': 'something'}
        form = SkillsForm(data=form_data)
        self.assertTrue(not form.is_valid())

        form_data = {
            'experienced': False,
            'level': 4,
        }
        form = SkillsForm(data=form_data)
        self.assertTrue(not form.is_valid())

class ProjectModelTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        my_admin = authenticate(username='myuser', password=password)
        self.client.login(username='myuser', password=password)

        response = self.client.post('/cv/project/new/', data={
            'title': 'proj wall',
            'description': 'this is what i did',
            'work_period': 'today'})
        new_item = Project.objects.first()  
        self.assertEqual(new_item.title, 'proj wall')
        self.assertEqual(new_item.description, 'this is what i did')
        self.assertEqual(new_item.work_period, 'today')
    
    def test_saving_and_retrieving_projects(self):
        initialCount = Project.objects.all().count()
        first_item = Project()
        first_item.title = 'intern'
        first_item.description = 'rezident evil gaming'
        first_item.work_period = 'back in the old days'
        first_item.save()

        second_item = Project()
        second_item.title = 'tester'
        second_item.description = 'drinking lots of water'
        second_item.work_period = '2021'
        second_item.save()

        current_items = Project.objects.all()
        self.assertEqual(current_items.count(), initialCount + 2)

        first_saved_item = current_items[0]
        second_saved_item = current_items[1]
        self.assertEqual(first_saved_item.title, 'intern')
        self.assertEqual(second_saved_item.description, 'drinking lots of water')

    def test_detect_invalid_exp_form(self):
        form_data = {'title': 'something'}
        form = ProjectForm(data=form_data)
        self.assertTrue(not form.is_valid())

        form_data = {
            'description': 'this is what i did',
            'work_period': 'remote',
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(not form.is_valid())

class InvolvementModelTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        my_admin = authenticate(username='myuser', password=password)
        self.client.login(username='myuser', password=password)

        response = self.client.post('/cv/involvement/new/', data={
            'name': 'wall',
            'role':'intern',
            'description': 'this is what i did',
            'work_period': 'today'})
        new_item = Involvement.objects.first()  
        self.assertEqual(new_item.name, 'wall')
        self.assertEqual(new_item.role, 'intern')
        self.assertEqual(new_item.description, 'this is what i did')
        self.assertEqual(new_item.work_period, 'today')
    
    def test_saving_and_retrieving_involvements(self):
        initialCount = Involvement.objects.all().count()
        first_item = Involvement()
        first_item.name = 'ella'
        first_item.role = 'intern'
        first_item.description = 'rezident evil gamer'
        first_item.work_period = 'back in the old days'
        first_item.save()

        second_item = Involvement()
        second_item.name = 'park'
        second_item.role = 'tester'
        second_item.description = 'drank water'
        second_item.work_period = '2021'
        second_item.save()

        current_items = Involvement.objects.all()
        self.assertEqual(current_items.count(), initialCount + 2)

        first_saved_item = current_items[0]
        second_saved_item = current_items[1]
        self.assertEqual(first_saved_item.name, 'ella')
        self.assertEqual(second_saved_item.work_period, '2021')

    def test_detect_invalid_exp_form(self):
        form_data = {'name': 'something'}
        form = InvolvementForm(data=form_data)
        self.assertTrue(not form.is_valid())

        form_data = {
            'role': 'intern',
            'description': 'this is what i did',
            'work_period': 'remote',
        }
        form = InvolvementForm(data=form_data)
        self.assertTrue(not form.is_valid())