from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from catalog.models import *

# Create your views here.

class catalog_list_view(ListView):
    model = catalogs
    context_object_name = "catalog_list"


class catalog_detail_view(DetailView):
    model = catalogs
    context_object_name = "catalog"
    template_name = "catalog/catalog_detail.html"