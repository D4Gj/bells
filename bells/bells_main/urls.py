from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Existing URL patterns
    # path('register/', views.registration_view, name='register'),
    path("login/", views.login_view, name="login"),
    path("create-bell/", views.CreateBellView.as_view(), name="create_bell"),
    path(
        "create-belltower/",
        views.CreateBellTowerView.as_view(),
        name="create_belltower",
    ),
    path("bell-list/", views.BellListView.as_view(), name="bell_list"),
    path("belltower-list/", views.BellTowerListView.as_view(), name="belltower_list"),
    path(
        "edit-belltower/<pk>/",
        views.BelltowerUpdateView.as_view(),
        name="edit_belltower",
    ),
    path(
        "create-movement-request/",
        views.create_bell_movement_request,
        name="create_bell_movement_request",
    ),
    path(
        "edit-movement-request/<int:pk>/",
        views.edit_bell_movement_request,
        name="edit_bell_movement_request",
    ),
    path(
        "movement-request/<int:pk>/",
        views.BellMovementRequestDetailView.as_view(),
        name="bell_movement_request_detail",
    ),
    path(
        "movement-requests/",
        views.BellMovementRequestListView.as_view(),
        name="bell_movement_request_list",
    ),
    path("edit-bell/<int:pk>/", views.edit_bell, name="edit_bell"),
    path('logout/', views.custom_logout, name='logout'),
    path("", views.HomeView.as_view(), name="home"),
]
