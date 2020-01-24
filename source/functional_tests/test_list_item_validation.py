#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tests.py
@Time    :   2020/01/23 11:48:22
@Author  :   Wang Liqiang
@Version :   1.0
@Contact :   richiewen8@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here input the import lib
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_duplicate_list_items(self):
        # 新建访问清单
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')
        # 重复
        inputbox = self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 错误信息
        self.wait_for(lambda :self.assertEqual(
            self.get_error_element().text,
            DUPLICATE_ITEM_ERROR
        ))
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        # 首页刷新显示一个错误信息
        # 提示办事项不能为空
        self.wait_for(lambda :self.browser.find_element_by_css_selector(
            '#id_text:valid'
            ))
        # 他输入一些文字
        # 错误消失
        inputbox = self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda :self.browser.find_element_by_css_selector(
            '#id_text:valid'
            ))
        # 现在能提交了
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 又提交了一个空的待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)
        # 她在列表中看到一条类型的错误
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda :self.browser.find_element_by_css_selector(
            '#id_text:valid'
            ))

        # 输入文字后就没有问题了
        inputbox = self.get_item_input_box().send_keys('Buy tea')
        self.wait_for(lambda :self.browser.find_element_by_css_selector(
            '#id_text:valid'
            ))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Buy tea')
    
    def test_error_messages_are_creared_on_input(self):
        # 出现错误验证
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')

        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda :self.assertTrue(
            self.browser.get_error_element().is_displayed()
        ))

        # 为了消除错误 输入内容
        self.get_item_input_box().send_keys('a')
        # 错误信息消失
        self.wait_for(lambda :self.assertFalse(
            self.get_error_element().is_displayed()
        ))

