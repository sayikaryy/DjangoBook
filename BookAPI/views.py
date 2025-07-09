from django.shortcuts import render, get_object_or_404
from .models import Book, Category
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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer   

class CustomerDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer  # assumes Customer exists
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] 

class CustomTokenView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access = response.data.get('access')
        refresh = response.data.get('refresh')

        # Set tokens as HttpOnly cookies
        res = Response({'message': 'Login successful'})
        res.set_cookie('access_token', access, httponly=True, secure=False, samesite='Lax')
        res.set_cookie('refresh_token', refresh, httponly=True, secure=False, samesite='Lax')
        return res
from rest_framework.views import APIView

class LogoutView(APIView):
    def post(self, request):
        res = Response({'message': 'Logged out'})
        res.delete_cookie('access_token')
        res.delete_cookie('refresh_token')
        return res