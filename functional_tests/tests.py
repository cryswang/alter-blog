
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
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        # c = Client()

        # # You'll need to log him in before you can send requests through the client
        # c.login(username=my_admin.username, password=password)

    def tearDown(self):  
        self.browser.quit()

    def test_can_make_post(self):  
         # Crystal is a student who makes semi-regular blog posts
         # centered around her budding career in software engineering
         # She opens up her blog, ready to make a new post about
         # a current topic she's exploring.

        self.browser.get(self.live_server_url)

        # However, she's quick to notice that she's logged out as the
        # plus icons indicating that she is able to make posts, are 
        # not visible.
        self.browser.find_elements_by_tag_name('span')

        # as the owner, she has to log in as an admin so she can make
        # posts. Thus, when she notices that she isn't logged in, she
        # navigates to the /admin url and inputs her credentials.
        self.browser.get('%s%s' % (self.live_server_url, '/admin/login/'))
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('myuser')
        password = self.browser.find_element_by_id('id_password')
        password.send_keys('mypassword')
        self.browser.find_element_by_xpath('//input[@value="Log in"]').click()
        
        time.sleep(1)

        # She sees then goes back to the homepage and checks that it's
        # loading properly.
        self.browser.get(self.live_server_url)
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
        post = posts[0].find_element_by_class_name('post-content')
        self.assertTrue(post.size['height'] < 600)

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  