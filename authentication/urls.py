from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import TokenView, ChangePasswordView, ResetPasswordView, \
    RegisterView, UsersView

urlpatterns = [
    path('login/', TokenView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UsersView.as_view({'get': 'list'}), name='users')
]
