from django.urls import path

from . import views

app_name = 'WGB'
urlpatterns = [
    path('', views.top_page, name='top'),
    path('login', views.show_login, name='show_login'),
    path('exe_login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create_user', views.create_user, name='create_user'),
    path('exe_create_user', views.execute_create_user, name='exe_create_user'),
    path('create_thread', views.create_thread, name='create_thread'),
    path('exe_create_thread', views.execute_create_thread, name='exe_create_thread'),
    path('thread<int:thread_no>/', views.show_thread, name='show_thread'),
    path('write_thread<int:thread_no>/', views.write_thread, name='write_thread'),
]