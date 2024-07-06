from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path("user/me/", User_Retrieve_SinId.as_view()),
    path("user/<int:pk>/", User_Retrieve.as_view()),
    path("user/<int:pk>/", User_Destroy.as_view(), name="delete-user"),
    path("user/<int:pk>/", User_Update.as_view(), name="update-user"),
    path("user/", User_List.as_view()),
    path("user/", User_Create.as_view()),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/logout/", Logout.as_view(), name="token_logout"),
]
