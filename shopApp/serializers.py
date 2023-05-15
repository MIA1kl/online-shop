from rest_framework import serializers
from .models import Category, Book, Cart, OrderItem
from .models import Comment
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = (
            'id',
            'title'
        )
        model = Category 
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'book', 'content', 'timestamp')


class BookSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username', read_only=False)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        fields = (
            'id',
            'title',
            'category',
            'author',
            'isbn',
            'pages',
            'price',
            'stock',
            'description',
            'imageUrl',
            'created_by',
            'status',
            'date_created', 
            'comments'
        )
        model = Book
        



class UserSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'books',
        )

class CartUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class CartSerializer(serializers.ModelSerializer):

    #Для вывода общей суммы, используется SerializerMethodField, который вызывает total_sum

    total_price = serializers.SerializerMethodField('total_sum')
    cart_id = CartUserSerializer(read_only=True, many=False)

    class Meta:
        model = Cart
        fields = ('cart_id', 'created_at', 'total_price')

     #Тут функция/метод total_sum работает засчёт обратной связи между моделями Cart и OrderItem.

    def total_sum(self, instance):
        total_price = 0
        for order_item in instance.order_items.all():
            total_price += order_item.book.price * order_item.quantity
        return total_price

        
    # def create(self, validated_data):
    #     books = validated_data['books']
    #     quantity = validated_data['quantity']
    #     cart_item_price = books.price * quantity

    #     cart = Cart.objects.create(books=books, quantity=quantity, total_price=total_price)
    #     return cart
        
# class OrderSerializer(serializers.ModelSerializer):

#     total_price = serializers.SerializerMethodField()

#     class Meta:
#         model = Order
#         fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'cart',
            'book',
        ]



class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=50, min_length=6)
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('username already exists')})

        return super().validate(args)
  

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)