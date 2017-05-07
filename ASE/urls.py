from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='home'),
    url(r'^student/(?P<entryNumber>\d{4}[a-zA-z]{2}\d{5})/$', views.student, name='student'),
    url(r'^faculty/(?P<id>\d+)/$', views.faculty, name='faculty'),
    url(r'^course/(?P<courseCode>[a-zA-Z0-9]+)/$', views.course, name='course'),
    url(r'^project/(?P<projectId>[0-9]+)/$', views.project, name='project'),
    url(r'^add/student/$', views.add_student, name='add_student'),
    url(r'^add/faculty/$', views.add_faculty, name='add_faculty'),
    url(r'^add/course/$', views.add_course, name='add_course'),
    url(r'^add/project/$', views.add_project, name='add_project'),
    url(r'^thanks/$', views.request_submitted, name='request_submitted'),
    url(r'^my_requests/$', views.my_requests, name='my_requests'),
    url(r'^show_request/(?P<requestId>[0-9]+)/$', views.show_request, name='show_request'),
    url(r'^moderate/$', views.moderate, name='moderate'),
    url(r'^moderate_request/(?P<requestId>[0-9]+)/$', views.moderate_request, name='moderate_request'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout')
]
