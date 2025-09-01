from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.list_categories, name="list_categories"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("item/comment/<str:item_id>", views.comment, name="comment"),
    path("item/close/<str:item_id>", views.close, name="close"),
    path("item/bid/<str:item_id>", views.bid, name="bid"),
    path("item/add/<str:item_id>", views.watchlist, name="add"),
    path("watchlist/delete/<str:item_id>", views.delete, name="delete"),
    path("item/<str:id>", views.item, name="item")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)