'''Imported Modules'''
from django.urls import path
from . import views
from . import api_views

app_name = 'news_app'

urlpatterns = [
    # User authentication
    path('', views.welcome, name='welcome'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('choose-group/', views.choose_group, name='choose_group'),
    path('home/', views.home, name='home'),

    # Publisher registration/view
    path('register/publisher/', views.register_under_publisher,
         name='register_under_publisher'),
    path('publisher/team/', views.publisher_team_view,
         name='publisher_team_view'),

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
    path('newsletter/read/<int:newsletter_id>/', views.read_newsletter,
         name='read_newsletter'),
    path('newsletter/update/<int:newsletter_id>/', views.update_newsletter,
         name='update_newsletter'),

    # Password reset
    path('password-reset/', views.send_password_reset_page,
         name='send_password_reset_page'),
    path('send-reset/', views.send_password_reset, name='send_password_reset'),
    # token_request handling
    path('reset-password/', views.token_request, name='token_request'),
    path('reset-password/update/', views.reset_password,
         name='reset_password'),
]

# API Endpoints
urlpatterns += [
    path('api/articles/', api_views.api_articles, name='api_articles'),
    path('api/articles/create/', api_views.api_create_article,
         name='api_create_article'),
    path('api/newsletters/', api_views.api_newsletters,
         name='api_newsletters'),
    path('api/newsletters/create/', api_views.api_create_newsletter,
         name='api_create_newsletter'),
]
