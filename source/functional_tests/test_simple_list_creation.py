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

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        # 伊迪斯听说话有一个很酷的在线待办事项应用
        # 她去看了这个网站的首页
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应邀输入一个待办事项
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # 在文本框中输入 "Buy peacock feathers"
        inputbox.send_keys('Buy peacock feathers')
        # 按回车键后 页面刷新
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        inputbox = self.get_item_input_box()
        # 按回车键后 页面刷新
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新 清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # 很满意  睡觉
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 伊迪斯新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 注意清单有个唯一URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        # 现在一名叫作弗朗西斯的新用户访问了网站

        # 我们使用一个新浏览器回话
        # 确保伊迪斯的信息不会从cookie泄露出去
        self.browser.close()
        self.browser = webdriver.Firefox()

        ## 弗朗西斯访问首页
        ## 页面看不到伊迪斯的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        # 弗朗西斯输入一个新的待办事项，新建一个清单
        # 他不想伊迪斯那样兴趣盎然
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 弗朗西斯获取了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        # 这个页面还是没有伊迪斯的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Buy milk',page_text)

        # 两个人都很满意，然后去睡觉