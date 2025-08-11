from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 登入登出註冊
    path('login/', TemplateView.as_view(template_name='registration/login.html'), name='login'),
    path('loginto/', views.login_view, name='loginto'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', TemplateView.as_view(template_name='registration/registrate.html'), name='register'),
    path('registerin/', views.register_view, name='registerin'),

    # 功能頁面
    path("melody/", views.melody, name="melody"),
    path('chat/<int:room_id>/', views.chat_room, name='chat-room'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit-message'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete-message'),
    path('upload_music/', views.upload_music, name='upload_music'),
    path('vote/<int:music_id>/', views.vote_view, name='vote'),
    path('music/<int:pk>/', views.music_detail, name='music_detail'),
    path('comments/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('music/<int:pk>/comment/', views.post_comment, name='post_comment'),

]
