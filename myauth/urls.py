from django.urls import path
from myauth import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('confirm_registration/', views.confirm_registration, name='confirm_registration'),
    path('reset/', views.reset_password_view, name='reset_password'),
    path('confirm_reset/', views.confirm_password_reset_view, name='confirm_password_reset'),
    path('change_password/', views.change_password_view, name='change_password'),
]
