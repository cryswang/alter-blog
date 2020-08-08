from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test.client import Client
from blog.views import post_list, bio_page, cv_page, post_detail
from blog.models import Post
from blog.forms import PostForm

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
    
    def test_can_save_a_POST_request(self):
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        my_admin = authenticate(username='myuser', password=password)
        self.client.login(username='myuser', password=password)
        response = self.client.post('/post/new/', data={'title':'something', 'text': 'this is text'})
        new_item = Post.objects.first()  
        self.assertEqual(new_item.title, 'something')
    
# class PostModelTest(TestCase):

    # def test_saving_and_retrieving_posts(self):
    #     # anonymous/null author error
    #     password = 'mypassword' 
    #     my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
    #     my_admin = authenticate(username='myuser', password=password)
    #     self.client.login(username='myuser', password=password)
    #     initialCount = Post.objects.all().count()
    #     first_item = Post()
    #     first_item.text = 'The first (ever) list item'
    #     first_item.save()

    #     second_item = Post()
    #     second_item.text = 'Item the second'
    #     second_item.save()

    #     current_items = Post.objects.all()
    #     self.assertEqual(current_items.count(), initialCount + 2)

        # because the blog displays posts in reverse chronoglogical order;
        # thus the most recent post should be at the top.
        # first_saved_item = current_items[1]
        # second_saved_item = current_items[0]
        # self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        # self.assertEqual(second_saved_item.text, 'Item the second')

    # test creating an invalid post

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
    
    # test to create a experience, 
    # create another and check they were ordered correctly
    # then be able to edit one
    # test objects count

    # test to create a project, 
    # create another and check they were ordered correctly
    # then be able to edit one
    # test objects count

    # test to create a skill, 
    # create another and check they were ordered correctly
    # test objects count

    # test to create an involvement, 
    # create another and check they were ordered correctly
    # then be able to edit one
    # test objects count