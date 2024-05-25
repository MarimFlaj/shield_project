"""
URL configuration for shield_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Im(port the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from shield.models import Url
from shield.views import SecureUrlView, UnSecureUrlView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shield.urls', namespace='shield')),

]
try :
    secure_urls=Url.objects.filter(type="secure")
    for url in secure_urls:
        urlpatterns.append(path(url.description, SecureUrlView.as_view()),)
    unsecure_urls=Url.objects.filter(type="unsecure")
    for url in unsecure_urls:
        urlpatterns.append(path(url.description, UnSecureUrlView.as_view(),{'template': url.template}),)
except Exception as e:
    print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeee",e)