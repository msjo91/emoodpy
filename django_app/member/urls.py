from django.urls import path

from . import views

app_name = "member"
urlpatterns = [
    path('signin/', views.signin_fbv, name='signin_p'),
    path('signin/research/', views.signin_fbv, name='signin_r'),
    path('signout/', views.signout_fbv, name='signout'),
    path('signup/', views.signup_fbv, name='signup'),
    path('profile/', views.profile_fbv, name='profile'),
    path('profile/change/', views.change_profile_fbv, name='change_profile'),
]
