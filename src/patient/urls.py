from django.conf.urls import url
from views import patientView


urlpatterns = [
    url(r'^patient/$', patientView),
]
