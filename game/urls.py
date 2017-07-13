from django.conf.urls import url
from game import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/login/$', views.login, {'template_name': 'game/login.html'}, name = 'login'),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'game/logout.html'}, name = 'logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^', views.home, name = 'home'),

]