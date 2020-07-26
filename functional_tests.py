
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

        # She sees her name of the browser of her website so she knows
        # it's loading properly.
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

        # When she does, she notices a typo (classic), and clicks on 
        # the post link to be taken to the post itself
        newPostLink = self.browser.find_element_by_tag_name('a').get_attribute('href')
        newPost = resolve(newPostLink)
        self.assertEqual(newPost.func, post_detail)

        # She then clicks on the edit button to edit the post

        # She saves her changes, then refreshes to see that her changes
        # are made.

        # Satsified, she logs off for the night
        self.fail('Finish the test!')  

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  