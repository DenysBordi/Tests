#-*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from uaprom.tests.selenium_tests.elements.base import Element, Block, Page
from uaprom.tests.selenium_tests.elements.drop_down_widget import \
    DropDownWidget


class EmployeesListBlock(Block):

    bann_manager_btn = Element(
        By.XPATH,
        u".//a[contains(text(), 'Заблокировать')]"
    )
    delete_manager_btn = Element(
        By.XPATH,
        u".//a[contains(text(), 'Удалить')]"
    )
    manager_info = Element.as_list(
        By.XPATH,
        ".//td[position()=3]"
    )


class FiltersBlock(Block):

    team_dd = DropDownWidget(By.XPATH, ".//*[@id='team_chosen']")
    search_input = Element(By.XPATH, ".//*[@id='query']")
    search_btn = Element(By.XPATH, ".//*[@id='submit_button']")


class CRMEmployeeListPage(Page):

    url = 'agency/agency/employee_list'

    result_message = Element(
        By.XPATH,
        ".//*[@id='cabinet_flash_message']//div[@class='h-layout-hidden']"
    )
    icon_success = Element(
        By.XPATH,
        ".//i[contains(@class,'icon-success')]"
    )
    team_select = Element(
        By.XPATH,
        ".//*[@id='team_choose_select']"
    )
    team_list_btn = Element(
        By.XPATH,
        ".//*[@id='team_list_button']"
    )
    create_manager_btn = Element(
        By.XPATH,
        ".//*[@id='client']"
    )
    employees_list_field = EmployeesListBlock.as_list(
        By.XPATH,
        "//*[@id='cabinet']//table[@class='item-list']//tr[not (./th)]")
    pager_link_list = Element.as_list(
        By.XPATH,
        ".//a[contains(@href, 'page_')]"
    )
    email_field = Element(
        By.XPATH,
        ".//*[contains(text(),'')]"
    )
    filters = FiltersBlock(
        By.XPATH,
        "//*[@id='search_employee_list_form']"
    )
    alert_accept_ban_btn = Element.as_list(
        By.XPATH,
        "//a[contains(@data-reactid, 'yes')]"
    ) #list because two identical locators

    def get_employee_row(self, manager_email):

        return self.employees_list_field.find(
            By.XPATH,
            ".//*[@id='cabinet']//table[@class='item-list']//tr[not (./th)]"
            "[./td[3][contains(text(),'%s')]]" % manager_email
        )

    def get_page_links(self):

        return [x.get_attribute("href") for x in self.pager_link_list][:-1] \
            if self.pager_link_list.is_present() else []

    def find_manager(self, team_name, manager_email):
        self.filters.team_dd.type_text_and_select_option(team_name)
        self.filters.search_input.set_value(manager_email)
        self.filters.search_btn.click()
