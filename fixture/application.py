from selenium import webdriver

from test.project_lib import ProjectMantisHelper
from fixture.session_helper import SessionHelper
from fixture.james import JamesHelper
from fixture.mail import MailHelper
from fixture.signup import SignupHelper
from fixture.soap import SoapHelper

class Application():
    def __init__(self, browser, config):
        if browser == 'firefox':
            self.wd = webdriver.Firefox()
        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
        elif browser == 'ie':
            self.wd = webdriver.Ie()
        else:
            raise ValueError('Unrecognize browser %s' % browser)

        self.session = SessionHelper(self)
        self.project = ProjectMantisHelper(self)
        self.config = config
        self.base_url = config['web']['baseUrl']
        self.james = JamesHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def restore(self):
        wd = self.wd
        wd.quit()
