from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BookViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomerDetailAPI, login_user, register_user, UserListView, CustomTokenView, LogoutView
from .views import OrderViewSet, UserViewSet, CartViewSet
from .views import CartView, CartItemDetailView
from .views import CustomTokenObtainPairView
from .views import AddToCartView
from .views import CheckoutView
from .views import AdminOrderViewSet

# ✅ Create router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'books', BookViewSet, basename='book')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'users', UserViewSet, basename='user')
router.register(r'orderadmin', AdminOrderViewSet, basename='orderadmin')

#router.register(r'cart', CartViewSet, basename='cart')



# ✅ urlpatterns
urlpatterns = [
    path('api/cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/', include(router.urls)),  # categories, books, orders, users, cart (viewsets)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Remove or rename this next one to avoid conflict
    # path('api/token/', login_user, name='login'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', register_user, name='register'),
    path('api/customer/', CustomerDetailAPI.as_view(), name='customer-detail'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/cart/', CartView.as_view()),
    path('api/cart/items/<int:item_id>/', CartItemDetailView.as_view()),
    path('api/checkout/', CheckoutView.as_view(), name='checkout'),
]
    


