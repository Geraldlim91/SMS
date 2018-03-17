from django.conf.urls import include, url
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^main/', include('src.login.urls'), ),
    url(r'^main/', include('src.register.urls')),
<<<<<<< HEAD
    url(r'^main/', include('src.checkupreminder.urls'))
=======
    url(r'^main/', include('src.patient.urls')),
>>>>>>> 5a4852bbe0fe58145c22fd72a0cec12a385ab606
]
