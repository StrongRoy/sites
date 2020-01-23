from django.urls import reverse

def get_url(name):
    return reverse(viewname=name)
