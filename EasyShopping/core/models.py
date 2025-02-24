from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    genderChoices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=genderChoices, default='Male', null=True, blank=True)
    
    dateOfBirth = models.DateField(null=True, blank=True, default=date(2000, 1, 1))
    userImage = models.ImageField(upload_to='customers/', null=True, blank=True, default='customers/userImageDefault.png')
    
    class Meta:
        db_table = 'customer'
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.username
    
class Category(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name_plural = "Categories"
        db_table = 'category'

    def __str__(self):
        return f"{self.categoryName}"
    
class Product(models.Model):
    productID = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    productName = models.CharField(max_length=255, null=False, default='Product Name')
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=False, default=100000) 
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    shippingFee = models.DecimalField(max_digits=6, decimal_places=0, default=0) 
    productImage = models.ImageField(upload_to='products/', null=False, blank=True, default='products/productImageDefault.png')

    productStatusChoices = (
        ("draft", "Draft"),
        ("disabled", "Disabled"),
        ("rejected", "Rejected"),
        ("in_review", "In Review"),
        ("published", "Published"),
    )
    productStatus = models.CharField(choices=productStatusChoices, max_length=10, default="Published") 
    featured = models.BooleanField(default=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(null = True, blank = True) 

    class Meta:
        verbose_name_plural = "Products"
        db_table = 'product'

    def getNewPrice(self):
        return self.price * (1 - self.discount)
    
    def __str__(self):
        return self.productName
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50px" height="50px" />' % (self.productImage.url))
    
class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'userInterest' 
    
class Size(models.Model):
    sizeID = models.AutoField(primary_key=True)  
    sizeName = models.CharField(max_length=50, null=False) 

    def __str__(self):
        return self.sizeName

    class Meta:
        db_table = 'size'

class Item(models.Model):
    itemID = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stockQuantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"{self.product} {self.size}"
    
    class Meta:
        db_table = 'item'

class Cart(models.Model):
    cartID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'item'], name='unique_cart_item')
        ]
        db_table = 'cartItem'

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  
    orderDate = models.DateTimeField(auto_now_add=True)
    orderAmount = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    itemQuantity = models.PositiveIntegerField(default=1)  
    statusChoices = (
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    orderStatus = models.CharField(max_length=10, choices=statusChoices, default='Processing') 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'item', 'orderDate'], name='unique_order_per_day')
        ]
        db_table = 'order'

class Review(models.Model):
    reviewID = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)

    RATING = (
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    )
    rating = models.IntegerField(choices=RATING, default=3)

    comment = models.TextField(null=True, blank=True)  
    reviewDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.productName

    class Meta:
        db_table = 'review'
        verbose_name_plural = "Product reviews"