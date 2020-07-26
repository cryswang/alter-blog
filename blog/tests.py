from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from blog.views import post_list, bio_page, cv_page, post_detail

class HomePageTest(TestCase):

    def test_root_url_resolves_to_blog(self):
        found = resolve('/')  
        self.assertEqual(found.func, post_list) 
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_bio_url_resolves_to_bio_page(self):
        found = resolve('/bio')  
        self.assertEqual(found.func, bio_page)
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/bio')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateUsed(response, 'blog/bio_page.html')
    
    def test_cv_url_resolves_to_cv_page(self):
        found = resolve('/cv')  
        self.assertEqual(found.func, cv_page)
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/cv')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateUsed(response, 'blog/cv_page.html')