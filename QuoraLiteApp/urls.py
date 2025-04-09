from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout, name="logout"),
    path("yourquestions", views.yourquestions, name="yourquestions"),
    path("viewall/<int:question_id>/", views.viewall, name="viewall"),
    path("liking/<int:answer_id>/", views.liking, name="liking"),
]
