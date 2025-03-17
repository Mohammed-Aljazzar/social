from django.urls import path
from .views import dashboard , profile_list, profile, all_users
from django.contrib.auth import views as auth_views

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),    
    path('logout/', auth_views.LogoutView.as_view(next_page='dwitter:login',http_method_names=['get', 'post']), name='logout'),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("all_users/", all_users, name="all_users"),
]

