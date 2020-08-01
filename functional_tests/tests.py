
import unittest
import django
import time
django.setup()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.http import HttpRequest
from django.urls import resolve
from blog.views import post_list, post_new, post_detail

class BlogOwnerTest(unittest.TestCase):  
    def setUp(self):  
        self.browser = webdriver.Chrome()

    def tearDown(self):  
        self.browser.quit()

    def test_can_make_post(self):  
         # Crystal is a student who makes semi-regular blog posts
         # centered around her budding career in software engineering
         # She opens up her blog, ready to make a new post about
         # a current topic she's exploring.

        self.browser.get('http://localhost:8000')

        # However, she's quick to notice that she's logged out as the
        # plus icons indicating that she is able to make posts, are 
        # not visible.
        self.assertTrue(len(self.browser.find_elements_by_tag_name('span')) < 1)

        # as the owner, she has to log in as an admin so she can make
        # posts. Thus, when she notices that she isn't logged in, she
        # navigates to the /admin url and inputs her credentials.
        self.browser.get('http://localhost:8000/admin')
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('cryswang')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('password')
        password.send_keys(Keys.ENTER)
        time.sleep(1)

        # She sees then goes back to the homepage and checks that it's
        # loading properly.
        self.browser.get('http://localhost:8000')
        self.assertIn('crystal w.', self.browser.title)  
        header = self.browser.find_element_by_tag_name('h1').find_element_by_tag_name('a')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('crystal', header_text)

        # Next to it, there's a "+" symbol to make a new post. She
        # clicks on it.
        self.assertEqual('glyphicon glyphicon-plus', self.browser.find_element_by_tag_name('span').get_attribute('class'))
        self.browser.get('http://localhost:8000/post/new')
        self.assertEqual('New Post', self.browser.find_element_by_tag_name('h2').get_attribute('innerHTML'))
        self.assertTrue(self.browser.find_element_by_class_name('post-form'))

        # She makes her new post and titles it Unit testing
        titleInput = self.browser.find_element_by_id('id_title')
        titleInput.send_keys('Unit Testing')

        # And writes a brief paragraph on what it is and how she
        # accomplishes it
        titleInput = self.browser.find_element_by_id('id_text')
        titleInput.send_keys('Unit testing is a very tedious procedure but is\n very necessary.')

        # She then goes down to the submit button and publishes the post
        submit = self.browser.find_element_by_tag_name('button')
        self.assertEqual('submit', submit.get_attribute('type'))
        submit.send_keys(Keys.ENTER)  
        time.sleep(1)
        
        # Then goes to the home page to see that it's there and it was
        # published correctly and also in the right order
        self.browser.get('http://localhost:8000')
        posts = self.browser.find_elements_by_class_name('post')
        self.assertTrue('Unit Testing', posts[0].find_element_by_tag_name('a').get_attribute('innerHTML'))

        # Then, she clicks on the new post to double check how it looks
        newPostLink = self.browser.find_element_by_tag_name('a').get_attribute('href')
        newPost = resolve(newPostLink)
        self.assertEqual(newPost.func, post_detail)

        # Satsified, she logs off for the night
        self.browser.quit()

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  