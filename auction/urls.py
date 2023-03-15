from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="auctionindex"),
    path("login", views.login_view, name="auctionlogin"),
    path("logout", views.logout_view, name="auctionlogout"),
    path("register", views.register, name="auctionregister"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("mine", views.mine, name="mine"),
    path("watching", views.watching, name="watching"),
    path("<int:user_id>/watch", views.watch, name="watch"),
    path("<int:user_id>/unwatch", views.unwatch, name="unwatch"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path("close", views.close, name="close"),
    path("category", views.category, name="category")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
