from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BookViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CustomerDetailAPI
from .views import RegisterView
from .views import UserListView
from .views import CustomTokenView
from .views import LogoutView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'books', BookViewSet, basename='book')
  # RegisterView for user registration
urlpatterns = [
    path('api/', include(router.urls)),
     path('api/token/', CustomTokenView.as_view(), name='token_obtain_pair'),  # login to get JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/customer/', CustomerDetailAPI.as_view(), name='customer-detail'),
     path('api/register/', RegisterView.as_view(), name='register'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

]

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjE0Mzk1NSwiaWF0IjoxNzUyMDU3NTU1LCJqdGkiOiIzNWM1OWU4MzljY2U0Y2ZkOWY4NDYxNDc4OGM2NzBmYSIsInVzZXJfaWQiOjJ9.se9Fzq_LwXyfp3gc6KeLZeHvM8ygdBmta3dXFbONT6E",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMDU3ODU1LCJpYXQiOjE3NTIwNTc1NTUsImp0aSI6ImIxZjAyZWFhM2U1ODRjZDRiZTBkNDkyYmRlZmFkYjNiIiwidXNlcl9pZCI6Mn0.pot2d2gSIvZcwxHXMECY-yoMcC1vCFtxQqmP3nuwGNo"
}