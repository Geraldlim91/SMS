from django.conf.urls import url
from views import patientView, patientAdd, patientViewUpdate, patientEdit,patientCaseAdd,caseViewUpdate
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^patient/$', patientView, name='patientView'),
    url(r'^patient/new/$', patientViewUpdate, name='patientViewUpdate'),
    url(r'^patient/case/new/(?P<nricvalue>\w+)$', caseViewUpdate, name='caseViewUpdate'),
    url(r'^patient/add/$', patientAdd, name='patientAdd'),
    url(r'^patient/editpatient/$', RedirectView.as_view(url=reverse_lazy('patientView')), name='patientEditUrl'),
    url(r'^patient/editpatient/(?P<nricvalue>\w+)$', patientEdit, name='patientEdit'),
    # url(r'^patient/addcase/$', RedirectView.as_view(url=reverse_lazy('patientView')), name='patientCaseAddUrl'),
    url(r'^patient/addcase/(?P<nricvalue>\w+)$',patientCaseAdd, name="patientCaseAdd")
]
