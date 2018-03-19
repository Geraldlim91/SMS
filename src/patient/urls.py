from django.conf.urls import url
from views import patientView, patientAdd, patientViewUpdate, patientEdit,patientCaseAdd,caseViewUpdate,issueDictionary, patientCaseView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^patient/$', patientView, name='patientView'),
    url(r'^patient/new/$', patientViewUpdate, name='patientViewUpdate'),
    url(r'^patient/case/new/(?P<nricvalue>\w+)$', caseViewUpdate, name='caseViewUpdate'),
    url(r'^patient/add/$', patientAdd, name='patientAdd'),
    url(r'^patient/editpatient/$', RedirectView.as_view(url=reverse_lazy('patientView')), name='patientEditUrl'),
    url(r'^patient/editpatient/(?P<nricvalue>\w+)$', patientEdit, name='patientEdit'),
    url(r'^patient/case/add/(?P<nricvalue>\w+)$',patientCaseAdd, name="patientCaseAdd"),

    url(r'^patient/case/view/(?P<idvalue>\w+)$',patientCaseView, name="patientCaseView"),
    url(r'^patient/case/view/$', RedirectView.as_view(url=reverse_lazy('patientView')), name='patientCaseViewUrl'),
    url(r'^dictionary/$',issueDictionary, name="issueDictionary")
]
