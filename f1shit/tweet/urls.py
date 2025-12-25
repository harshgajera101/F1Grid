from django.urls import path
from . import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path(
    'react/<int:tweet_id>/<str:reaction_type>/',
    views.react_to_tweet,
    name='react_to_tweet'),
    path('api/drivers/', views.get_drivers_by_team, name='get_drivers_by_team'),
    # path('poll/vote/<int:option_id>/', views.vote_poll, name='vote_poll'),
    path('poll/vote/<int:option_id>/', views.poll_vote, name='poll_vote'),
    path("profile/<str:username>/", views.profile_view, name="profile"),
]
