'''Imported Modules'''
from django.urls import path
from . import views

app_name = 'news_app'

urlpatterns = [
    # User authentication
    path('', views.welcome, name='welcome'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('choose-group/', views.choose_group, name='choose_group'),
    path('home/', views.home, name='home'),

    # Publisher registration
    path('register/publisher/', views.register_under_publisher,
         name='register_under_publisher'),

    # Subscriptions
    path('subscribe/', views.subscribe, name='subscribe'),

    # Articles / Newsletters
    path('articles/', views.article_list,
         name='article_list'),
    path('articles/mine/', views.view_mine,
         name='view_mine'),
    path('article/view/<int:article_id>/', views.view_article,
          name='view_article'),
    path('subscribed/', views.subscribed_articles,
         name='subscribed_articles'),
    path('article/read/<int:article_id>/', views.read_article,
         name='read_article'),
    path('article/update/<int:post_id>/', views.update_post,
         name='update_post'),
    path('article/remove/<int:post_id>/', views.remove_post,
         name='remove_post'),
    path('article/create/', views.create_post, name='create_post'),
    path('article/publish/', views.publish_post, name='publish_post'),

    # Password reset
     path('password-reset/', views.send_password_reset_page, name='send_password_reset_page'),
     path('send-reset/', views.send_password_reset, name='send_password_reset'),
     # token_request handling
     path('reset-password/', views.token_request, name='token_request'),
     path('reset-password/update/', views.reset_password, name='reset_password'),
]

# API Endpoints
urlpatterns += [
    path('api/articles/', views.article_list, name='api_article_list'),
    path('api/articles/mine/', views.view_mine, name='api_view_mine'),
    path('api/article/<int:article_id>/', views.view_article, name='api_view_article'),
    path('api/subscribe/', views.subscribe, name='api_subscribe'),
    path('api/article/create/', views.create_post, name='api_create_post'),
    path('api/article/update/<int:post_id>/', views.update_post, name='api_update_post'),
    path('api/article/remove/<int:post_id>/', views.remove_post, name='api_remove_post'),
]
