from django.conf.urls import include, url
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^main/', include('src.login.urls'), ),
    url(r'^main/', include('src.register.urls')),
]
