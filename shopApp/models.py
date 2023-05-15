from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    author = models.CharField(max_length=100, default='unknown')
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    price = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField()
    imageUrl = models.URLField()
    created_by = models.ForeignKey('auth.User', related_name='books', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)
    comments = models.ManyToManyField('Comment', related_name='books', blank=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title


class Cart(models.Model):
    cart_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    '''
    Закоментировал эти части кода.. Так как смысла в них не было и через связь M2M не заработало подсчитывание общей суммы.
    
    
    Скорее всего не работало по причине того, что поле M2M сохранялось после метода - save(). Что было причиной, того
    что оно было пустой
    '''

    # books = models.ManyToManyField(Book)
    # quantity = models.IntegerField(default=1)
    # total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    # def calculate_total_price(self):
    #     total = 0
    #     for book in self.books.all().iterator():
    #         print(book)
    #         total += book.price * self.quantity
    #     return total

    # def save(self, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     print(self.books)
    #     super().save(*args, **kwargs)
    #     self.total_price = self.calculate_total_price()
    #     super().save()

    # class Meta:
    #     ordering = ['cart_id', '-created_at']

    def __str__(self):
        return f"{self.cart_id}"


class OrderItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='order_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='order_books')
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.cart.cart_id} books - {self.book.title}"


# class Order(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     total_price = models.FloatField(default=0, blank=True, null=True)
#     creation_date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-creation_date']

#     def __str__(self):
#         return f"{self.id} Total price: {self.total_price}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments', blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
