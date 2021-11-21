from django.urls import path
from .views import LoginView, ProfileView

app_name = "user"
urlpatterns = [
    path("login", view=LoginView.as_view(), name="user_login"),
    path("profile", view=ProfileView.as_view(), name="user_profile"),
]
