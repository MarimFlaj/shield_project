
from django.urls import path


def update_secure_urls(url,UrlView):
    from shield_project.urls import urlpatterns
    urlpatterns.append(path(url.description, UrlView.as_view()),)
    
