from rest_framework import serializers
from .models import CartItem, Category, Book
from django.contrib.auth.models import User
from .models import Customer
from .models import Order, OrderItem




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'price',
            'stock',
            'description',
            'category',
            'image',       # ✅ Accept uploaded image
            'image_url'    # ✅ Provide absolute URL for display
        ]
        extra_kwargs = {
            'image': {'write_only': True}  # Hide raw path in response if you want
        }

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Customer
        fields = ['user', 'phone', 'address']
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        # Create linked Customer automatically
        Customer.objects.create(user=user)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# class OrderItemSerializer(serializers.ModelSerializer):
#     book_title = serializers.CharField(source='book.title', read_only=True)
    
#     class Meta:
#         model = OrderItem
#         fields = ['book_title', 'quantity']
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book', 'quantity']

    def create(self, validated_data):
        order = validated_data.get('order')
        if not order:
            raise serializers.ValidationError("Order is required.")
        return OrderItem.objects.create(**validated_data)


from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'book_title', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(many=True)  # or use related_name if set
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_ordered', 'status', 'items', 'total_amount']

    def get_total_amount(self, obj):
        return sum(item.book.price * item.quantity for item in obj.items.all())


    
class CartItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_price = serializers.DecimalField(source='book.price', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_title', 'book_price', 'quantity']
    