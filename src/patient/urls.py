from django.conf.urls import url
from views import patientView, patientAdd


urlpatterns = [
    url(r'^patient/$', patientView),
    url(r'^patient/add/$', patientAdd),
]
