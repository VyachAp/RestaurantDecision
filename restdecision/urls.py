from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from restdecision.views.restaurant import RestaurantView
from restdecision.views.menu import MenuView, MenuVotesView, UploadMenuView, VoteView
from restdecision.views.register import RegisterView, CreateUserView

app_name = "restdecision"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("users/create/", CreateUserView.as_view(), name="create_user"),
    path("restaurants/", RestaurantView.as_view(), name="restaurants"),
    path("restaurants/<int:restaurant_id>/menu/", MenuView.as_view(), name="menus"),
    path(
        "restaurants/actions/upload_menu/", UploadMenuView.as_view(), name="upload_menu"
    ),
    path("menus/votes/", MenuVotesView.as_view(), name="menu_votes"),
    path("menus/actions/vote", VoteView.as_view(), name="vote_for_menu"),
]

schema_view = get_schema_view(
    openapi.Info(title="Restaurant Decision API", default_version="v1"),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
    authentication_classes=[],
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + urlpatterns
