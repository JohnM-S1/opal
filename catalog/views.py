from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import urllib.request
import json
from catalog.models import *
from control_profile.models import profile, imports
from component_definition.models import components


# Create your views here.

class catalog_list_view(ListView):
    model = catalogs
    context_object_name = "context_list"
    template_name = "generic_list.html"


class catalog_detail_view(DetailView):
    model = catalogs
    context_object_name = "context"
    template_name = "generic_detail.html"


class control_detail_view(DetailView):
    model = controls
    context_object_name = "context"
    template_name = "generic_detail.html"


def import_catalog_view(request, catalog_link):
    """
    Imports a pre-defined set of catalogs
    """
    from common.views import available_catalog_list

    for item in available_catalog_list:
        if catalog_link == item["slug"] and not catalogs.objects.filter(uuid=item['uuid']).exists():
            catalog_url = item["link"]
            f = urllib.request.urlopen(catalog_url)
            catalog_json = json.loads(f.read().decode('utf-8'))
            catalog_dict = catalog_json["catalog"]
            new_catalog = catalogs()
            new_catalog.import_oscal(catalog_dict)
            new_catalog.save()

            # create a new profile for the imported catalog
            new_metadata = metadata.objects.create(title=new_catalog.metadata.title)
            new_profile = profile.objects.create(
                metadata=new_metadata
                )
            new_profile.save()
            url = "https://" + request.get_host() + new_catalog.get_permalink()
            new_profile.imports.add(imports.objects.create(href=url, import_type="catalog"))
            new_profile.save()

            # create components for any groups in the catalog
            for group in new_catalog.groups.all():
                new_component = components.objects.get_or_create(
                    type="policy",
                    title=group.title + " Policy",
                    description="This Component Policy was automatically created durring the import of " + new_metadata.title,
                    purpose="This Component Policy was automatically created durring the import of " + new_metadata.title,
                    status="under-development"
                    )

            context = {'msg': new_catalog.metadata.title + " imported from " + catalog_url}
            # return render(request, "index.html", context)
    return redirect('home_page')
