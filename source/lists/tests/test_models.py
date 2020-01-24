#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_models.py
@Time    :   2020/01/23 11:50:33
@Author  :   Wang Liqiang
@Version :   1.0
@Contact :   richiewen8@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here input the import lib

from lists.models import Item,List
from django.test import TestCase as DjangoTest
from django.core.exceptions import ValidationError
class ListAndItemModelsTest(DjangoTest):
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item,list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_,text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1,text='bla')
        item = Item.objects.create(list=list2,text='bla')
        item.full_clean()
        
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1,text='i1')
        item2 = Item.objects.create(list=list1,text='item 2')
        item3 = Item.objects.create(list=list1,text='3')

        self.assertEqual(
            list(Item.objects.all()),
            [item1,item2,item3]
        )
        
    def test_string_reprentation(self):
        item = Item(text='some text')
        self.assertEqual(str(item),'some text')

class ItemModelTest(DjangoTest):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text,'')

class ListModeTest(DjangoTest):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(),f'/lists/{list_.id}/')