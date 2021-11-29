"""opal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import os
import environ
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve(strict=True).parent.parent)

env = environ.Env()
if os.path.exists(BASE_DIR + "/opal/.env"):
    environ.Env.read_env()
else:
    print("Warning!!!  No .env file found, using default environment variables")
    environ.Env.read_env("opal/defaults.env")


urlpatterns = [
    path('', include('ssp.urls'), name='index'),
    path('admin/', admin.site.urls, name='admin'),
    path('tinymce/', include('tinymce.urls')),
]

if env("ADFS_ENABLED") == "True":
urlpatterns.append(path('oauth2/', include('django_auth_adfs.urls')))