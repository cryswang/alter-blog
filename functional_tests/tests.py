
import time
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import resolve
from selenium import webdriver
from django.http import HttpRequest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from blog.views import post_list, post_new, post_detail

class BlogOwnerTest(LiveServerTestCase):  
    def setUp(self):  
        self.browser = webdriver.Chrome()

        # as the owner, she has to log in as an admin so she can make
        # posts. Thus, when she notices that she isn't logged in, she
        # navigates to the /admin url and inputs her credentials.
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        self.browser.get('%s%s' % (self.live_server_url, '/admin/login/'))
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('myuser')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('mypassword')
        self.browser.find_element_by_xpath('//input[@value="Log in"]').click()
        time.sleep(1)
        self.browser.get(self.live_server_url)

    def tearDown(self):  
        self.browser.quit()

    def test_can_make_post(self):  
         # Crystal is a student who makes semi-regular blog posts
         # centered around her budding career in software engineering
         # She opens up her blog, ready to make a new post about
         # a current topic she's exploring.
        
        self.assertIn('crystal w.', self.browser.title)  
        header = self.browser.find_element_by_tag_name('h1').find_element_by_tag_name('a')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('crystal', header_text)

        # Next to it, there's a "+" symbol to make a new post. She
        # clicks on it.
        self.assertEqual('glyphicon glyphicon-plus', self.browser.find_element_by_tag_name('span').get_attribute('class'))
        self.browser.get('%s%s' % (self.live_server_url, '/post/new/'))
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
        self.browser.get(self.live_server_url)
        posts = self.browser.find_elements_by_class_name('post')
        self.assertTrue('Unit Testing', posts[0].find_element_by_tag_name('a').get_attribute('innerHTML'))
        post = posts[0].find_element_by_class_name('post_content')
        self.assertTrue(post.size['height'] < 600)
    
    def test_can_update_cv(self):  
        self.browser.get('%s%s' % (self.live_server_url, '/cv'))
        icons = self.browser.find_elements_by_tag_name('span')
        for icon in icons:
            self.assertEqual('glyphicon glyphicon-plus', icon.get_attribute('class'))
        self.assertEqual(5, len(icons))
        
        self.assertEqual('Education.', self.browser.find_elements_by_tag_name('h3')[0].get_attribute('innerHTML'))

        self.assertEqual('Experiences.', self.browser.find_elements_by_tag_name('h3')[1].get_attribute('innerHTML'))
        self.browser.get('%s%s' % (self.live_server_url, '/cv/experience/new/'))
        header = self.browser.find_element_by_tag_name('h2')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('New Experience', header_text)
        self.assertTrue(self.browser.find_element_by_class_name('post-form'))

        # She makes her new post and titles it Unit testing
        companyInput = self.browser.find_element_by_id('id_company')
        companyInput.send_keys('Unit Testing')

        # She makes her new post and titles it Unit testing
        titleInput = self.browser.find_element_by_id('id_title')
        titleInput.send_keys('Unit Tester')

        # And writes a brief paragraph on what it is and how she
        # accomplishes it
        descriptionInput = self.browser.find_element_by_id('id_description')
        descriptionInput.send_keys('Unit testing is a very tedious procedure but is\n very necessary.')
        
         # She makes her new post and titles it Unit testing
        locationInput = self.browser.find_element_by_id('id_title')
        locationInput.send_keys('testing land')

         # She makes her new post and titles it Unit testing
        workInput = self.browser.find_element_by_id('id_title')
        workInput.send_keys('now until forever')

        # She then goes down to the submit button and publishes the post
        submit = self.browser.find_element_by_tag_name('button')
        self.assertEqual('submit', submit.get_attribute('type'))
        submit.send_keys(Keys.ENTER)  
        time.sleep(1)
        
        # It should automatically redirect back to /cv for her to see that it's there and
        # published correctly in the right order
        experiences = self.browser.find_elements_by_class_name('exp')
        self.assertTrue('Unit Testing', experiences[0].find_element_by_tag_name('h1').get_attribute('innerHTML'))
        title = experiences[0].find_element_by_tag_name('h2').get_attribute('innerHTML')

        # self.assertEqual('Projects.', self.browser.find_elements_by_tag_name('h3')[2].get_attribute('innerHTML'))
        # self.assertEqual('Skills.', self.browser.find_elements_by_tag_name('h3')[3].get_attribute('innerHTML'))
        # self.assertEqual('Involvement.', self.browser.find_elements_by_tag_name('h3')[4].get_attribute('innerHTML'))

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  