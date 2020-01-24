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
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
            # Edith goes to the home page
            self.browser.get(self.live_server_url)
            self.browser.set_window_size(1024, 768)

            # She notices the input box is nicely centered
            inputbox= self.get_item_input_box()
            self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=10
            )

