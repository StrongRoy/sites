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
from lists.models import Item,List
from django.urls import reverse

class HomePageTest(DjangoTest):

    def test_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get(reverse('home'))
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(DjangoTest):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(reverse('view_list',args=(list_.id,)))
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(reverse('view_list',args=(correct_list.id,)))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response,'other list item 1')
        self.assertNotContains(response,'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()
        response = self.client.get(reverse('view_list',args=(correct_list.id,)))
        self.assertEqual(response.context['list'],correct_list)

class NewListTest(DjangoTest):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            reverse('add_item',args=(correct_list.id,)),
            data={'item_text':"A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list,correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response  = self.client.post(
            reverse('add_item', args=(correct_list.id,)),
            data={'item_text': "A new item for an existing list"}
        )
        self.assertRedirects(response,reverse('view_list',args=(correct_list.id,)))

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(reverse('new_list'), data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertRedirects(response,reverse('view_list',args=(new_list.id,)))