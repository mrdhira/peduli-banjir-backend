from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token
from .views import LoginView, ProfileView, GenerateTokenView

app_name = "user"
urlpatterns = [
    path("login", view=LoginView.as_view(), name="user_login"),
    path("profile", view=ProfileView.as_view(), name="user_profile"),
    path("generate-token", view=GenerateTokenView.as_view(), name="generate_token"),
    path("refresh-token", refresh_jwt_token, name="refresh_token"),
]
