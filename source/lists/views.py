from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Item, List


# Create your views here.

def home_page(request):
    return render(request, 'home.html')


def view_list(request,list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        try:
            item = Item.objects.create(text=request.POST.get('item_text',''),list=list_)
            item.full_clean()
            item.save()
            return redirect(reverse('view_list',args=(list_.id,)))
        except ValidationError:
            error = "You can't have an empty list item."
    return render(request, 'list.html', {'list': list_,"error":error})