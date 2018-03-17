from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^checkupreminder/$', views.reminder ),
]
