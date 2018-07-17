# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from uaprom.tests.selenium_tests.elements.base import Block, Element
from uaprom.tests.selenium_tests.elements.checkbox import Checkbox
from uaprom.tests.selenium_tests.elements.select_drop_down import SelectDropDown


class ManagerListForAttachmentCompanies(Block):

    all_managers_chkbx = Checkbox(
        By.XPATH,
        ".//input[@name='select-all-managers']"
    )
    submit_btn = Element(
        By.XPATH,
        ".//*[@id='submit_submit']"
    )
    team_select = SelectDropDown(
        By.XPATH,
        ".//*[@id='team-selector']"
    )
