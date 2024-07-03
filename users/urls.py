from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig

from users.views import PaymentsListAPIView, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDeleteAPIView, PaymentsCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    # Токены
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Платежи
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
    path("payment/create/", PaymentsCreateAPIView.as_view(), name="payment-create"),

    # Пользователь
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('', UserListAPIView.as_view(), name='user-list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user-delete'),
]
