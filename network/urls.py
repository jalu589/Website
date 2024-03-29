from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="networkindex"),
    path("login", views.login_view, name="networklogin"),
    path("logout", views.logout_view, name="networklogout"),
    path("register", views.register, name="networkregister"),
    path('user/<int:user_id>', views.user, name="user"),
    path('following', views.following, name="following"),

    path("newpost", views.newpost, name="newpost"),
    path('follow', views.follow, name="follow"),
    path('edit/<int:post_id>', views.edit, name="edit"),
    path('like/<int:post_id>', views.like, name="like")
]
