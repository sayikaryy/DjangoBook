from django.shortcuts import render, get_object_or_404
from .models import Book, Category, Customer
from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer, BookSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomerSerializer
from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .serializers import UserSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import RegisterSerializer
from .models import Order, OrderItem, Cart, CartItem
from .serializers import OrderItemSerializer, OrderSerializer
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CartItemSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend










class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']  # For ?category=1
    search_fields = ['title', 'author']  # For ?search=python

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        # DEBUG: Print everything coming from frontend
        print("\n--- DEBUG START ---")
        print("request.data:", dict(request.data))
        print("request.FILES:", request.FILES)
        if 'image' in request.FILES:
            print("Image file name:", request.FILES['image'].name)
            print("Image content type:", request.FILES['image'].content_type)
        else:
            print("No image found in request.FILES")
        print("--- DEBUG END ---\n")

        return super().create(request, *args, **kwargs)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items', 'items__book', 'customer__user').all()
    serializer_class = OrderSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
class CartViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('book', 'order').all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        # For now, return all items (you can filter by user if you have auth)
        items = OrderItem.objects.select_related('book').all()
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        item = self.get_object()
        quantity = request.data.get("quantity")
        if quantity and int(quantity) > 0:
            item.quantity = int(quantity)
            item.save()
            return Response(self.get_serializer(item).data)
        return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CustomerDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer  # assumes Customer exists
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        # Send JWT in HttpOnly cookies
        response = Response({
            "message": "Login successful",
            "is_admin": user.is_staff  # Return role only
        }, status=status.HTTP_200_OK)

        # Set cookies (HttpOnly = safer)
        response.set_cookie('access', str(refresh.access_token), httponly=True, secure=False)
        response.set_cookie('refresh', str(refresh), httponly=True, secure=False)

        return response
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Saves user in SQLite
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        original_response = super().post(request, *args, **kwargs)
        if original_response.status_code != 200:
            return original_response

        access = original_response.data.get('access')
        refresh = original_response.data.get('refresh')

        res = Response({"message": "Login successful"})
        res.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=False,    # False on localhost HTTP dev
            samesite='Lax',
            max_age=30000,
            path='/',
        )
        res.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=7*24*3600,
            path='/',
        )
        return res

    
from rest_framework.views import APIView

class LogoutView(APIView):
    def post(self, request):
        res = Response({'message': 'Logged out'})
        res.delete_cookie('access_token')
        res.delete_cookie('refresh_token')
        return res

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = [{
        "id": item.id,
        "quantity": item.quantity,
        "book": {
            "id": item.book.id,
            "title": item.book.title,
            "price": item.book.price
        }
    } for item in cart.items.all()]
    return Response(items)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    book_id = request.data.get("book_id")
    quantity = int(request.data.get("quantity", 1))
    book = Book.objects.get(id=book_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    return Response({"message": "Item added to cart"})

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Fetching cart for user:", request.user.username)
        cart, created = Cart.objects.get_or_create(user=request.user)
        print(f"Cart created? {created}, Cart ID: {cart.id}")
        items = CartItem.objects.filter(cart=cart)
        print(f"Number of items in cart: {items.count()}")
        for i in items:
            print(f"Item: {i.book.title}, Quantity: {i.quantity}")
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)


    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        book_id = request.data.get("book_id")
        quantity = int(request.data.get("quantity", 1))  # Convert to int

        try:
            book = Book.objects.get(id=book_id)
            item, created = CartItem.objects.get_or_create(cart=cart, book=book)

            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity

            item.save()
            return Response({"detail": "Added to cart!", item: item}, status=201)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=404)

class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart_and_item(self, request, item_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            item = CartItem.objects.get(cart=cart, id=item_id)
            return cart, item
        except CartItem.DoesNotExist:
            return cart, None

    def put(self, request, item_id):
        cart, item = self.get_cart_and_item(request, item_id)
        if not item:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")
        if quantity is None:
            return Response({"detail": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity < 1:
                return Response({"detail": "Quantity must be at least 1"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"detail": "Quantity must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        item.quantity = quantity
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data)

    def delete(self, request, item_id):
        cart, item = self.get_cart_and_item(request, item_id)
        if not item:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
    
class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra data
        data['is_admin'] = self.user.is_staff  # or is_superuser if preferred
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
     def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            # Set the HttpOnly cookies
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=3600,  # 1 hour
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=7 * 24 * 3600,  # 7 days
            )

            # Optionally remove tokens from response body
            del response.data['access']
            del response.data['refresh']
        return response
    
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("== DEBUG START ==")
        print("Authenticated User:", request.user)
        print("Is Authenticated:", request.user.is_authenticated)
        print("Request Data:", request.data)
        print("Authorization Header:", request.headers.get("Authorization"))
        print("== DEBUG END ==")

        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            book = Book.objects.get(id=book_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
            cart_item.quantity += quantity
            cart_item.save()

            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    book_id = request.data.get('book_id')
    quantity = int(request.data.get('quantity', 1))

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    cart, _ = Cart.objects.get_or_create(user=user)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    return Response({"message": "Added to cart!"})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    try:
        order = Order.objects.get(customer=request.user.customer, is_ordered=False)
    except Order.DoesNotExist:
        return Response([])

    items = OrderItem.objects.filter(order=order)
    serializer = OrderItemSerializer(items, many=True)
    return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Return orders only for current logged-in user
        return self.queryset.filter(customer__user=self.request.user)
    
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)

        if not items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create order with the customer instance
        order = Order.objects.create(customer=customer, status='Pending')

        # Create order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
            )

        # Clear cart
        items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
@login_required
@api_view(['GET'])
def cart_view(request):
    order = Order.objects.filter(customer=request.user.customer, complete=False).first()
    if not order:
        return Response([])  # No cart yet

    items = OrderItem.objects.filter(order=order)
    serializer = OrderItemSerializer(items, many=True)
    return Response(serializer.data)



class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items', 'items__book', 'customer__user')
    serializer_class = OrderSerializer
  