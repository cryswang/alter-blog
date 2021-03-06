
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

class OwnerTest(LiveServerTestCase):  
    def setUp(self):  
        self.browser = webdriver.Chrome()

        # as the owner, she has to log in as an admin so she can make
        # posts. Thus, when she notices that she isn't logged in, she
        # goes to /admin and enters in her credentials.
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

        # The post should be less than 600px tall; any post with content
        # exceeding it should be cut off
        post = posts[0].find_element_by_class_name('post_content')
        self.assertTrue(post.size['height'] < 600)
    
    def test_can_update_cv(self):  
        # To prepare for recruiting season, Crystal wants to update
        # her cv to match all of her newest qualification and everything
        # she's learned thus far. She goes to her CV page and sees that
        # she has the option to add new sections.
        self.browser.get('%s%s' % (self.live_server_url, '/cv'))
        icons = self.browser.find_elements_by_tag_name('span')
        for icon in icons:
            self.assertEqual('glyphicon glyphicon-plus', icon.get_attribute('class'))
        self.assertEqual(5, len(icons))

        # She first decides to add a new experience, so she clicks on the plus
        # icon in the experiences section
        self.browser.get('%s%s' % (self.live_server_url, '/cv/experience/new/'))
        header = self.browser.find_element_by_tag_name('h2')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('New Experience', header_text)
        self.assertTrue(self.browser.find_element_by_class_name('post-form'))

        # She fills in the info about the last place she worked at and
        # what she did
        companyInput = self.browser.find_element_by_id('id_company')
        for i in range(7):
            companyInput.send_keys(Keys.BACKSPACE)
        companyInput.send_keys('Unit Testing')
        titleInput = self.browser.find_element_by_id('id_title')
        for i in range(6):
            titleInput.send_keys(Keys.BACKSPACE)
        titleInput.send_keys('Unit Tester')
        descriptionInput = self.browser.find_element_by_id('id_description')
        for i in range(4):
            descriptionInput.send_keys(Keys.BACKSPACE)
        descriptionInput.send_keys('Unit testing is a very tedious procedure but is very necessary.')
        locationInput = self.browser.find_element_by_id('id_location')
        for i in range(15):
            locationInput.send_keys(Keys.BACKSPACE)
        locationInput.send_keys('testing land')
        workInput = self.browser.find_element_by_id('id_work_period')
        for i in range(12):
            workInput.send_keys(Keys.BACKSPACE)
        workInput.send_keys('now until forever')

        # She then goes down to the submit button and saves the new experience
        # to her blog
        submit = self.browser.find_element_by_tag_name('button')
        self.assertEqual('submit', submit.get_attribute('type'))
        submit.send_keys(Keys.ENTER)  
        time.sleep(1)
        
        # It should automatically redirect back to /cv for her to see that it's there and
        # published correctly in the right order
        experiences = self.browser.find_elements_by_class_name('exp')
        self.assertEqual('Unit Testing', experiences[0].find_element_by_tag_name('h1').get_attribute('innerHTML'))
        title = experiences[0].find_element_by_tag_name('h2').get_attribute('innerHTML')
        self.assertEqual('Unit Tester', title)
        desc = experiences[0].find_element_by_class_name('desc').find_element_by_tag_name('p').get_attribute('innerHTML')
        self.assertEqual('Unit testing is a very tedious procedure but is very necessary.', desc)
        info = experiences[0].find_element_by_class_name('additional_info')
        self.assertEqual('now until forever', info.find_elements_by_tag_name('p')[0].find_element_by_tag_name('b').get_attribute('innerHTML'))
        self.assertEqual('testing land', info.find_elements_by_tag_name('p')[1].find_element_by_tag_name('b').get_attribute('innerHTML'))

        # she also picked up a few skills along the way from the internship, and would
        # like to add them onto her cv. She begins by clicking the + icon by the skills
        # section
        self.browser.get('%s%s' % (self.live_server_url, '/cv/skill/new/'))
        header = self.browser.find_element_by_tag_name('h2')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('New Skill', header_text)
        self.assertTrue(self.browser.find_element_by_class_name('post-form'))

        # She adds her new skill; she's experienced in it, but it's still not her top skill,
        # so she ranks it at a 1, which is just behind the 0th (top) skill.
        titleInput = self.browser.find_element_by_id('id_title')
        for i in range(5):
            titleInput.send_keys(Keys.BACKSPACE)
        titleInput.send_keys('Django')
        self.assertEqual('True', self.browser.find_element_by_id('id_experienced').get_attribute('value'))
        levelInput = self.browser.find_element_by_id('id_level')
        levelInput.send_keys(Keys.UP)

        # She then goes down to the submit button and adds the skill
        submit = self.browser.find_element_by_tag_name('button')
        self.assertEqual('submit', submit.get_attribute('type'))
        submit.send_keys(Keys.ENTER)  
        time.sleep(1)

        self.browser.get('%s%s' % (self.live_server_url, '/cv/skill/new/'))
        header = self.browser.find_element_by_tag_name('h2')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('New Skill', header_text)
        self.assertTrue(self.browser.find_element_by_class_name('post-form'))

        # She adds her new skill; she's not super experienced in it, but is
        # still somewhat familiar, so she ranks it as her top inexperienced skill
        titleInput = self.browser.find_element_by_id('id_title')
        for i in range(5):
            titleInput.send_keys(Keys.BACKSPACE)
        titleInput.send_keys('Python')
        self.browser.find_element_by_id('id_experienced').click()

        # She then goes down to the submit button and adds the skill
        submit = self.browser.find_element_by_tag_name('button')
        self.assertEqual('submit', submit.get_attribute('type'))
        submit.send_keys(Keys.ENTER)  
        time.sleep(1)
        
        # It should automatically redirect back to /cv for her to see that it's there and
        # published correctly in the right order
        skills_box = self.browser.find_element_by_class_name('skills_box')
        self.assertEqual('Django', skills_box.find_element_by_class_name('skill_e').get_attribute('innerHTML'))
        self.assertEqual('Python', skills_box.find_element_by_class_name('skill_f').get_attribute('innerHTML'))
    
    def test_can_add_involvement_and_project(self):  
        # Crystal recently got involved in a new group and worked on
        # a project that she'd like to add to her cv. She goes to the cv
        # page and first decides to add the project she worked on
        # with the group
        self.browser.get('%s%s' % (self.live_server_url, '/cv'))
        self.browser.get('%s%s' % (self.live_server_url, '/cv/project/new/'))
        header = self.browser.find_element_by_tag_name('h2')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('New project', header_text)
        self.assertTrue(self.browser.find_element_by_class_name('post-form'))

        # She fills in the fields of the form to describe what she did
        titleInput = self.browser.find_element_by_id('id_title')
        for i in range(7):
            titleInput.send_keys(Keys.BACKSPACE)
        titleInput.send_keys('Unit Tester')
        descriptionInput = self.browser.find_element_by_id('id_description')
        for i in range(4):
            descriptionInput.send_keys(Keys.BACKSPACE)
        descriptionInput.send_keys('Unit testing is a very tedious procedure but is very necessary.')
        workInput = self.browser.find_element_by_id('id_work_period')
        for i in range(12):
            workInput.send_keys(Keys.BACKSPACE)
        workInput.send_keys('now until forever')

        # She then goes down to the submit button and saves the project
        # to her blog
        submit = self.browser.find_element_by_tag_name('button')
        self.assertEqual('submit', submit.get_attribute('type'))
        submit.send_keys(Keys.ENTER)  
        time.sleep(1)
        
        # It should automatically redirect back to /cv for her to see that it's there and
        # published correctly in the right order
        projects = self.browser.find_elements_by_class_name('projects')
        self.assertEqual('Unit Tester', projects[0].find_element_by_tag_name('h1').get_attribute('innerHTML'))
        work_period = projects[0].find_element_by_tag_name('h2').get_attribute('innerHTML')
        self.assertEqual('now until forever', work_period)
        desc = projects[0].find_element_by_tag_name('p').get_attribute('innerHTML')
        self.assertEqual('Unit testing is a very tedious procedure but is very necessary.', desc)

        # She would then like to add the involvement--the group she was
        # a part of. from the cv page, she clicks on the add button and goes to the
        # new involvement form.
        self.browser.get('%s%s' % (self.live_server_url, '/cv/involvement/new/'))
        header = self.browser.find_element_by_tag_name('h2')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('New involvement', header_text)
        self.assertTrue(self.browser.find_element_by_class_name('post-form'))

        # she fills out all the necessary info
        nameInput = self.browser.find_element_by_id('id_name')
        for i in range(12):
            nameInput.send_keys(Keys.BACKSPACE)
        nameInput.send_keys('uob css')
        roleInput = self.browser.find_element_by_id('id_role')
        for i in range(6):
            roleInput.send_keys(Keys.BACKSPACE)
        roleInput.send_keys('new member')
        descriptionInput = self.browser.find_element_by_id('id_description')
        for i in range(4):
            descriptionInput.send_keys(Keys.BACKSPACE)
        descriptionInput.send_keys('attending balls and secret after parties')
        workInput = self.browser.find_element_by_id('id_work_period')
        for i in range(12):
            workInput.send_keys(Keys.BACKSPACE)
        workInput.send_keys('march 2020')

        # She then goes down to the submit button and saves the involvement to
        # her blog
        submit = self.browser.find_element_by_tag_name('button')
        self.assertEqual('submit', submit.get_attribute('type'))
        submit.send_keys(Keys.ENTER)  
        time.sleep(1)
        
        # It should automatically redirect back to /cv for her to see that it's there and
        # published correctly in the right order
        invs = self.browser.find_elements_by_class_name('involvement')
        self.assertEqual('uob css', invs[0].find_element_by_tag_name('h1').get_attribute('innerHTML'))
        self.assertEqual('new member', invs[0].find_element_by_tag_name('h2').get_attribute('innerHTML'))
        self.assertEqual('march 2020', invs[0].find_element_by_tag_name('h3').get_attribute('innerHTML'))
        self.assertEqual('attending balls and secret after parties', invs[0].find_element_by_tag_name('p').get_attribute('innerHTML'))

class VisitorTest(LiveServerTestCase):  
    def setUp(self):  
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)

    def tearDown(self):  
        self.browser.quit()

    def test_view_bio_page(self):  
         # Erin is a recruiter who is visiting the website to scope
         # out the newest candidate. She lands on the home page and
         # sees who the website belongs to
        
        self.assertIn('crystal w.', self.browser.title)  
        header = self.browser.find_element_by_tag_name('h1').find_element_by_tag_name('a')
        header_text = header.get_attribute('innerHTML')
        self.assertIn('crystal', header_text)

        # Since she's just a visitor, there's no way to add new posts
        try:
            self.browser.find_element_by_tag_name('span')
        except NoSuchElementException:
            pass
        
        # Although there is an option to log in, if she has an account
        login = self.browser.find_element_by_class_name('login')
        self.assertEqual('login.', login.get_attribute('innerHTML'))
        
        # To learn more about the candidate, she first checks out the bio
        # page and reads the short description
        self.browser.get('%s%s' % (self.live_server_url, '/bio'))
        bio1 = '<p><b>Hi! I\'m Crystal</b>, an upcoming-fourth year undergraduate CS student. I\'m interested in <b>front-end web development</b> and <b>full stack engineering</b>, although there are countless other fields I\'d love to explore <i>(such as UX)</i>.</p>'
        bio2 = '<p>I like to read mysteries and watch action shows, and spend my weekends cooking and, occassionally, writing. You can check out my projects on <a href=\"https://github.com/cryswang\">github</a> and connect with me on <a href=\"https://www.linkedin.com/in/crystal-wang-72885759/\">linkedin</a>.</p>'
        bio3 = '<p><b>Thanks for stopping by!</b></p>'
        bio = bio1 + '<br>' + bio2 + '<br>' + bio3
        browserBio = "".join(self.browser.find_element_by_class_name('bio').get_attribute('innerHTML').split("\n"))
        self.assertEqual(bio, browserBio)
    
    def test_view_cv_page(self):  
        # She then navigates to the cv page to view the candidate's
        # qualifications.

        self.browser.get('%s%s' % (self.live_server_url, '/cv'))

        # Once again, she's unable to add any new experiences etc.
        # since she's only a visitor.
        try:
            self.browser.find_element_by_tag_name('span')
        except NoSuchElementException:
            pass
        
        # The first thing she reads is the "education" section, which is
        # static

        desc = []
        desc.append('Currently pursuing a <b>B.S. in Computer Science </b>')
        desc.append('with a <b>Creative Writing Minor</b> and an alumni of the')
        desc.append('<i>Advanced Cybersecurity Experience for Students</i>')
        desc.append('Honors College, also known as <b>ACES</b>.')

        edu = self.browser.find_element_by_class_name('edu')
        self.assertEqual('University of Maryland, College Park', edu.find_element_by_tag_name('h1').get_attribute('innerHTML'))
        educationDesc = edu.find_element_by_class_name('desc').find_elements_by_tag_name('p')
        for i in range(4):
            self.assertEquals(educationDesc[i].get_attribute('innerHTML'), desc[i])
        
        titles = edu.find_element_by_class_name('additional_info').find_elements_by_tag_name('h2')
        self.assertEquals('gpa', titles[0].get_attribute('innerHTML'))
        self.assertEquals('grad. date', titles[1].get_attribute('innerHTML'))
        info = edu.find_element_by_class_name('additional_info').find_elements_by_tag_name('p')
        self.assertEquals('3.6 / 4.0', info[0].get_attribute('innerHTML'))
        self.assertEquals('may 2021', info[1].get_attribute('innerHTML'))

        # Erin scrolls down and notes that there are other sections to the cv. it's currently
        # empty, so it seems this blog still is a work in progress, but at least the sections
        # are there.

        self.assertEqual('Experiences.', self.browser.find_elements_by_tag_name('h3')[1].get_attribute('innerHTML'))
        self.assertEqual('Projects.', self.browser.find_elements_by_tag_name('h3')[2].get_attribute('innerHTML'))
        self.assertEqual('Skills.', self.browser.find_elements_by_tag_name('h3')[3].get_attribute('innerHTML'))
        self.assertEqual('Involvement.', self.browser.find_elements_by_tag_name('h3')[4].get_attribute('innerHTML'))

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  