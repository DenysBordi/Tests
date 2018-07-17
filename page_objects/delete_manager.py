#-*- coding: utf-8 -*-
from uaprom.tests.selenium_tests.util import common as c
from selenium.webdriver.common.by import By
from uaprom.tests.selenium_tests.elements.base import Element, Page
from uaprom.tests.selenium_tests.crm.page_objects.blocks.manager_list_for_attachment_companies import ManagerListForAttachmentCompanies


class CRMDeleteManagerPage(Page):

    url = 'agency/delete_manager/'

    title_page = Element(
        By.XPATH,
        ".//*[@id='cabinet']//h1"
    )
    manager_list_field = ManagerListForAttachmentCompanies(
        By.XPATH,
        ".//form[@name='rebind_companies_form']"
    )
