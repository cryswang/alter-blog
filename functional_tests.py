from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Chrome()

    def tearDown(self):  
        self.browser.quit()

    def test_can_make_post(self):  
        # User first comes to the home page of the app
        self.browser.get('http://localhost:8000')

        # The name of the browser is my website
        self.assertIn('crystal', self.browser.title)  
        self.fail('Finish the test!')  

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  