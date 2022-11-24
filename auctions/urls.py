from django.urls import path

from auctions import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("category/<str:entry>", views.entry, name="entry"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("bidding/<int:id>", views.bidding, name="bidding"),
    path("commenting/<int:id>", views.commenting, name="commenting"),
    path("watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("close/<int:id>", views.close_listing, name="close_listing"),

]
