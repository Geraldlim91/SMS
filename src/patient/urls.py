from django.conf.urls import url
from views import patientView, patientAdd, patientViewUpdate


urlpatterns = [
    url(r'^patient/$', patientView),
    url(r'^patient/new/$', patientViewUpdate, name='patientViewUpdate'),
    url(r'^patient/add/$', patientAdd, name='patientAdd'),
]
