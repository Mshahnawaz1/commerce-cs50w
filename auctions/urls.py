from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add/<int:item_id>", views.add_watchlist,  name="add_watchlist"),
    path("bid/", views.bid, name="bid"),
    path("close/", views.close_auction, name="close_auction"),
    path("comment/", views.comment, name="comment")

]
