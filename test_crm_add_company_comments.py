#-*- coding: utf-8 -*-

from datetime import datetime, timedelta

from uaprom.tests.selenium_tests.test_setup.test_case.test_case import ChromeSuit
from uaprom.tests.selenium_tests.util import common as c
from uaprom.tests.selenium_tests.util import users
from uaprom.tests.selenium_tests.crm.page_objects.company_comments import CRMCompanyCommentsPage
from uaprom.tests.selenium_tests.test_setup.test_case.test_case import ds_ctx


def get_tomorrow_date():
    delta = timedelta(days=1)
    return (datetime.now() + delta).strftime('%d.%m.%Y')


def select_event_date_and_random_time(self, date):
    ccp = CRMCompanyCommentsPage(self.driver)
    ccp.comment_block.date_input.send_keys(date)
    ccp.comment_block.click()  # to close datepicker
    ccp.next_event_time_drop_down.select_random_option()
    ccp.comment_block.scheduled_events_quality.wait_to_display()


class TestCRMAddComments(ChromeSuit):

    def test_add_company_comment_for_admin(self):
        data_setup = ds_ctx()
        test_company = data_setup.get_random_company_id(
            service_id=0, agency_ids=[1])
        self.sign_in(users.Admin.email)
        ccp = CRMCompanyCommentsPage(self.driver)
        self.get_url(
            self.base_url_my + ccp.admin_url % test_company
        )
        ccp.add_comment_link.click()
        event_type_admin = ccp.comment_block.comment_event_type_drop_down.\
            wait_to_display().select_random_options()
        comment = self.fake.text(max=100)
        ccp.comment_block.comment_input.set_value(comment)
        ccp.comment_block.preview_button.click()
        self.soft_assert_in(
            comment,
            ccp.preview_comment_form.preview_comment_text.text,
            "Another preview text for comment"
        )
        ccp.preview_comment_form.close_btn.click()
        ccp.comment_block.save_comment_button.click()
        ccp.comment_filter_type_drop_down.wait_to_display(
            ).select_option_by_text(event_type_admin)
        ccp.submit_filter_btn.click()
        c.wait_for_page_loaded(self.driver)

        self.soft_assert_true(
            ccp.find_comment_left(event_type_admin, comment),
            "No expected comment"
        )
        author = ccp.get_comments_author()[0]

        self.soft_assert_equals(
            author,
            ' '.join(users.Admin.name.split()),
            "Not admin user's comment"
        )

    def test_add_company_comment_for_manager(self):
        data_setup = ds_ctx()
        company_id = data_setup.get_random_company_id(service_id=29)
        manager = data_setup.get_company_manager(company_id)

        self.sign_in(manager["email"])
        ccp = CRMCompanyCommentsPage(self.driver)
        self.get_url(self.base_url_my + ccp.crm_url
                     % company_id)
        ccp.add_comment_link.click()
        ccp.add_stats_link.click()
        ccp.wait_for_page_loaded()
        ccp.comment_block.contact_type_drop_down.wait_to_display(

        ).select_random_options()
        event_type_crm = ccp.comment_block.comment_event_type_drop_down.\
            wait_to_display().select_random_options()
        select_event_date_and_random_time(self, get_tomorrow_date())
        if ccp.selectable_stages.is_present():
            ccp.click_random_selectable_stage()
        ccp.comment_block.save_comment_button.click()
        ccp.comment_filter_type_drop_down.wait_to_display(
            ).select_option_by_text(event_type_crm)
        ccp.submit_filter_btn.click()
        self.soft_assert_true(
            ccp.find_comment_left(event_type_crm, u'Товаров, услуг:'),
            "No expected comment"
        )
        author = ccp.get_comments_author()[0]
        self.soft_assert_equals(
            author,
            ' '.join(manager["name"].split()),
            "Not crm user's comment"
        )
