from django.conf.urls import url

from .views import TestPage

app_name = 'shop'

urlpatterns = [
    url(r'^$', TestPage.as_view(), name='index'),
]
