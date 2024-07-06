from django.urls import path

from .views import *

urlpatterns = [
    path("admin/logout/", logout_view),
    path("logout/", logout_view),
    path("", admin_view),
]
