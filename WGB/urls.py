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
    path('join_member/', views.join_member, name='join_member'),
    path('show_join_thread_list/', views.show_join_thread_list, name='show_join_thread_list'),
    path('show_sender_list/thread<int:thread_no>/member<int:member_id>', views.show_sender_list, name='show_sender_list'),
    path('send_message/thread<int:thread_no>/member<int:member_id>', views.send_message, name='send_message'),
    path('exe_send_message/', views.exe_send_message, name='exe_send_message'),
    path('show_message/<int:message_id>/<int:member_object_id>', views.show_message, name='show_message'),
]