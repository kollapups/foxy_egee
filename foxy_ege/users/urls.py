from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("callback/", views.oauth_callback, name="callback"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path(
        "profile/<str:subject>/create-homework/",
        views.create_homework,
        name="create_homework",
    ),
    path(
        "profile/<str:subject>/get-homework/", views.get_homework, name="get_homework"
    ),
    path(
        "profile/<str:subject>/submit-homework/",
        views.submit_homework,
        name="submit_homework",
    ),
    path(
        "profile/<str:subject>/homework/<int:homework_id>/",
        views.homework_detail,
        name="homework_detail",
    ),
]
