from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, YoView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('yo/', YoView.as_view(), name='yo'),
]
