import pytest
import logging
from faker import Faker
from pages.areas_page import AreasConstants
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
import random
import string
import os

class TestAddArea:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        # Initialize logger
        self.logger = logging.getLogger(self.__class__.__name__)

        # Initialize other attributes
        self.faker = Faker()
        self.add_category_page = AddCategoryPage(driver)
        self.categories_page = CategoriesPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config

         # Login and navigate to add category page
        self.driver.get(f"{self.config.base_url}/login")
        self.login_page.login(self.config.username, self.config.password)
        self.side_menu.expand_system_settings()
        self.side_menu.navigate_to_system_settings_item('areas')
        self.categories_page.click_new_category()
