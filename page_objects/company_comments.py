# -*- coding: utf-8 -*-
import random
from selenium.webdriver.common.by import By
from uaprom.tests.selenium_tests.elements.select_drop_down import SelectDropDown
from uaprom.tests.selenium_tests.elements.base import Element, Block, Page
from uaprom.tests.selenium_tests.elements.drop_down_widget import DropDownWidget


class PreviewCommentBlock(Block):
    preview_comment_text = Element(
          By.CSS_SELECTOR,
          "#markdownPanel"
    )
    close_btn = Element(
          By.CSS_SELECTOR,
          ".ui-icon-closethick"
    )

class AddCommentBlock(Block):
    contact_type_drop_down = DropDownWidget(
        By.ID,
        'add_comment_contact_type_chosen'
    )
    comment_event_type_drop_down = DropDownWidget(
        By.ID,
        'add_comment_event_type_chosen'
    )
    save_comment_button = Element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    )
    date_input = Element(
        By.NAME,
        'add_comment-next_event_date'
    )
    comment_input = Element(
        By.CSS_SELECTOR,
        '[name=add_comment-comment]'
    )
    scheduled_events_quality = Element(
        By.CSS_SELECTOR,
        '.js-scheduled-events-quantity'
    )
    preview_button = Element(
        By.CSS_SELECTOR,
        ".wmd-button.wmd-preview-button"
    )


class CommentsListBlock(Block):
    comment_headers = Element.as_list(
        By.CSS_SELECTOR,
        '.comment-header'
    )
    comment_bodies = Element.as_list(
        By.CSS_SELECTOR,
        '.comment-header + tr'
    )
    comment_headers_author = Element.as_list(
        By.XPATH,
        "//*[@class = 'comment-header']//td[5]/span"
    )


class CRMCompanyCommentsPage(Page):
    add_comment_link = Element(
        By.CSS_SELECTOR,
        '.js-add-comment-link'
    )
    add_stats_link = Element(
        By.CSS_SELECTOR,
        '.js-insert-stats-link'
    )
    next_event_time_drop_down = SelectDropDown(
        By.ID,
        'add_comment-next_event_time'
    )
    selectable_stages = Element.as_list(
        By.XPATH,
        '//li[contains(@class, "js-selectable-choice")]'
        '[not(@data-stage="REJECTION")]//*'
        '[@class="b-stages__item-text js-stage-title"]'
    )
    current_stage = Element(
        By.XPATH,
        '//li[contains(@class, "b-stages__item_state_active")]'
        '//*[@class="b-stages__item-text js-stage-title"]'
    )
    cancellation_stage = Element(
        By.XPATH, "//*[(@data-stage='REJECTION')]"
    )
    disabled_stages = Element.as_list(
        By.CSS_SELECTOR, ".b-stages_state_disable.js-disabled"
    )

    comment_type_all_btn = Element(
        By.XPATH,
        ".//*[@id = 'comment_type_all']"
    )
    comment_type_system_btn = Element(
        By.XPATH,
        ".//*[@id = 'comment_type_system']"
    )
    comment_type_manual_btn = Element(
        By.XPATH,
        ".//*[@id = 'comment_type_manual']"
    )
    submit_filter_btn = Element(
        By.XPATH,
        u".//*[@value = 'Отфильтровать']"
    )
    comment_filter_type_drop_down = DropDownWidget(
        By.ID,
        'event_type_chosen'
    )

    add_comment_block = AddCommentBlock(
        By.XPATH,
        './/*[contains(@class,"b-agency-client-add-comment-form__form-fields-container")]'
    )
    comment_block = AddCommentBlock(
        By.XPATH,
        './/*[contains(@class,"b-agency-client-add-comment-form__form-fields-container")]'
    )
    preview_comment_form = PreviewCommentBlock(
        By.CSS_SELECTOR,
        ".preview_panel"
    )
    comments_list = CommentsListBlock(
        By.XPATH,
        "//*[@id='comment_list_container']/table/tbody"
    )
    current_manager_block = Element(By.CSS_SELECTOR, ".agency_client_manager_info")

    crm_url = 'agency/crm/company_comments/%s'
    admin_url = 'admin/crm/company_comments/%s'

    def find_comment_left(self, comment_type, comment_text):
        comments = zip(
            self.comments_list.comment_headers,
            self.comments_list.comment_bodies
        )
        for comment_line in comments:
            if comment_type.lower() in comment_line[0].text.lower() \
                    and comment_text.lower() in comment_line[1].text.lower():
                return True
        else:
            return False

    def get_comments_author(self):
        return [x.text for x in self.comments_list.comment_headers_author]

    def click_random_selectable_stage(self):
        random_stage = random.choice(self.selectable_stages)
        if self.disabled_stages.is_present():
            self.cancellation_stage.click()
            random_stage.click()
        else:
            random_stage.click()
        return random_stage.text
