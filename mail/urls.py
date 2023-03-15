from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="mailindex"),
    path("login", views.login_view, name="maillogin"),
    path("logout", views.logout_view, name="maillogout"),
    path("register", views.register, name="mailregister"),

    # API Routes
    path("emails", views.compose, name="compose"),
    path("emails/<int:email_id>", views.email, name="email"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"),
]