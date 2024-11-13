from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tracker/', views.index, name='tracker'),
    path('get_recommendations/', views.get_recommendations, name='get_recommendations'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),  # Update to the correct view name
    path('logout/', views.logout_user, name='logout'),
    path('tracker/',views.tracker,name="tracker"),
    path('profile/',views.profile_view,name="profile"),
    path('period_tracker',views.period_tracker,name="period_tracker"),
    path("messages/", views.inbox, name="inbox"),
    path("messages/send/", views.send_message, name="send_message"),
    path("messages/<uuid:message_id>/", views.message_detail, name="message_detail"),
]
