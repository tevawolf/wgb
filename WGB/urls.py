from django.urls import path

from . import views

app_name = 'WGB'
urlpatterns = [
    path('', views.top_page, name='top'),
    path('login', views.show_login, name='show_login'),
    path('exe_login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create_user', views.create_user, name='create_user'),
    path('exe_create', views.execute_create_user, name='exe_create_user'),
]