from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="user-registration"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.UserDetailView.as_view(), name='user-detail'),  # Added route for current user details
]
