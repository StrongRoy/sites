#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_views.py
@Time    :   2020/01/23 11:45:41
@Author  :   Wang Liqiang
@Version :   1.0
@Contact :   richiewen8@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here input the import lib

from django.test import TestCase as DjangoTest
from django.urls import reverse
from django.utils.html import escape
from unittest import skip

from lists.models import Item,List
from lists.forms import ItemForm,EMPTY_ITEM_ERROR,DUPLICATE_ITEM_ERROR,ExistingListItemForm
class HomePageTest(DjangoTest):

    def test_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get(reverse('home'))
        self.assertEqual(Item.objects.count(), 0)
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'],ItemForm)


class ListViewTest(DjangoTest):
    # 使用Django 测试客户端
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html') # 检查使用的模板，然后在上下文中检查各个待办事项
    def test_passes_correct_list_to_template(self):
        correct_list=List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'],correct_list) # 检查每个对象都是希望的到的，或者查询集合中包含正确的待办事项
    def test_display_items_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        # print(response.content.text)
        self.assertIsInstance(response.context['form'], ExistingListItemForm) # 检查表单使用正确的类
        self.assertContains(response, 'name="text"')
    
    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)

        response = self.client.get(reverse('view_list',args=(correct_list.id,)))

        self.assertContains(response, 'itemey 1') # 检查测试模板逻辑：每个for if 都要做最简单的测试
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response,'other list item 1')


    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/',
            data={'text':"A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(),1) # 对于处理POST请求的视图，确保有效和无效两种情况都要测试
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list,correct_list)

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()
        response  = self.client.post(
            reverse('view_list', args=(correct_list.id,)),
            data={'text': "A new item for an existing list"}
        )
        self.assertRedirects(response,reverse('view_list',args=(correct_list.id,)))
    
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )


    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR)) # 健全性检查，检查是否渲染指定表单，而且是否有错误信息

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1,text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data = {'text':'textey'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


