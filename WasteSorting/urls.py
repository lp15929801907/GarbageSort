"""WasteSorting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from MyApp import views as App_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('MyApp/', include('MyApp.urls')),
    path('login/', App_views.login),
    path('common_register/', App_views.common_register),
    path('manager_register/', App_views.manager_register),
    path('login_judge/', App_views.login_judge),
    path('common_information/', App_views.common_information),
    path('garbage_type/', App_views.garbage_type),
    path('search_dump/', App_views.search_dump),
    path('throw_record/', App_views.throw_record),
    path('search_record/', App_views.search_record),
    path('change_password/', App_views.change_password),
    path('throw_dump/', App_views.throw_dump),
    path('delete_record/', App_views.delete_record),
    path('manager_information/', App_views.manager_information),
    path('manage_dump/', App_views.manage_dump),
    path('delete_dump/', App_views.delete_dump),
    path('add_dump/', App_views.add_dump),
    path('reduce_dump/', App_views.reduce_dump),
    path('change_manager_password/', App_views.change_manager_password),
    path('add_new_dump/', App_views.add_new_dump),
    path('alter_dump/', App_views.alter_dump),
    path('common_analysis/', App_views.common_analysis),
    path('manage_analysis/', App_views.manage_analysis),
    path('manage_common/', App_views.manage_common),
    path('delete_common/', App_views.delete_common),
    path('', App_views.login),
]
