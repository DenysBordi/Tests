#-*- coding: utf-8 -*-
import pytest
from faker import Faker

from uaprom.tests.selenium_tests.test_setup.test_case.test_case import ChromeSuit
from uaprom.tests.selenium_tests.crm.page_objects.employee_list import CRMEmployeeListPage
from uaprom.tests.selenium_tests.crm.page_objects.delete_manager import CRMDeleteManagerPage
from uaprom.tests.selenium_tests.test_setup.test_case.test_case import ds_ctx

crm_email = "test@prom.ua.test"
team_id_list = [165]
company_id = 27960
fake = Faker()

manager_companies = [
    ('has companies', True),
    ('have not companies', False)
]


class TestCRMBanAndDeleteManager(ChromeSuit):

    manager_id = None

    def test_search_ban_manager(self):
        data_setup = ds_ctx()
        self.sign_in(crm_email)

        manager_first_name = fake.first_name()
        manager_last_name = fake.last_name()
        manager_email = fake.safe_email()

        self.manager_id = data_setup.create_manager(
            manager_first_name,
            manager_last_name,
            manager_email,
            company_id,
            team_id_list
        )["id"]

        self.get_url(
            self.base_url_my + CRMEmployeeListPage.url)

        employee_list_page = CRMEmployeeListPage(self.driver)
        employee_list_page.find_manager(
            u'Консультационная', manager_email
        )
        created_manager = employee_list_page.get_employee_row(
            manager_email=unicode(manager_email)
        )
        created_manager.bann_manager_btn.lookup().click()
        employee_list_page.alert_accept_ban_btn[1].click() #list index
        employee_list_page.icon_success.wait_to_display()
        employee_list_page.find_manager(
            u'Консультационная', manager_email
        )
        self.soft_assert_in(
            u"Статус: заблокирован",
            created_manager.manager_info.text,
            "Found status is not as expected"
        )

    @pytest.mark.parametrize('has_companies', manager_companies)
    def test_delete_manager(self, has_companies):
        data_setup = ds_ctx()
        self.sign_in(crm_email)

        manager_first_name = fake.first_name()
        manager_last_name = fake.last_name()
        manager_email = fake.safe_email()

        self.manager_id = data_setup.create_manager(
            manager_first_name,
            manager_last_name,
            manager_email,
            company_id,
            team_id_list
        )["id"]

        if has_companies[1]:  # The point of using parameter
            data_setup.bind_company_to_manager(self.manager_id)

        self.get_url(
            self.base_url_my + CRMEmployeeListPage.url +
            '?team_id={team_id}'.format(team_id=team_id_list[0])
        )
        employee_list_page = CRMEmployeeListPage(self.driver)
        created_manager = employee_list_page.get_employee_row(
            manager_email=unicode(manager_email))
        created_manager.delete_manager_btn.lookup().click()
        employee_list_page.alert_accept_ban_btn.click()

        delete_manager_page = CRMDeleteManagerPage(self.driver)
        name = ' '.join([manager_first_name, manager_last_name])
        self.soft_assert_equals(
            delete_manager_page.title_page.text,
            u"Удаление менеджера %s" % name,
            "Found status is not as expected"
        )
        delete_manager_page.manager_list_field.team_select.select_by_visible_text(
            u'Все команды')
        delete_manager_page.manager_list_field.all_managers_chkbx.select()
        delete_manager_page.manager_list_field.submit_btn.click()
        employee_list_page.icon_success.wait_to_display()
        self.soft_assert_element_is_present(
            employee_list_page.icon_success,
            "Error:Icon of success do not displayed"
        )

        links = employee_list_page.get_page_links()
        links.append(
            self.driver.current_url +
            '?team_id={team_id}'.format(team_id=team_id_list[0])
        )
        for link in links:
            if employee_list_page.get_employee_row(
                    manager_email).is_present():
                self.soft_assert_in(
                    u"Статус: удален",
                    created_manager.manager_info.text,
                    "Found status is not as expected"
                )
                break
            self.get_url(link)

    def custom_teardown_method(self):
        data_setup = ds_ctx()
        if self.manager_id:
            data_setup.delete_manager(self.manager_id)
