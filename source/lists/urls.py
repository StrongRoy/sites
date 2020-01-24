
from django.urls import path
from . import views

urlpatterns = [
    path('<int:list_id>/', views.view_list, name='view_list'),

]