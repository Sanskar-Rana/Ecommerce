from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
STATE_CHOICE = (
    ('Provicion 1','Provicion 1'),
    ('Provicion 2','Provicion 2'),
    ('Provicion 3','Provicion 3'),
    ('Provicion 4','Provicion 4'),
    ('Provicion 5','Provicion 5'),
    ('Provicion 6','Provicion 6'),
    ('Provicion 7','Provicion 7')
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    contactNumber = models.IntegerField()
    state = models.CharField(choices = STATE_CHOICE, max_length=20)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('Helmet','Helmet'),
    ('Accessories','Accessories'),
    ('Tyres','Tyres'),
    ('Jersey','Jersey'),
    ('Lubricant', 'Lubricant'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices= CATEGORY_CHOICES, max_length=15)
    product_image = models.ImageField(upload_to = 'productimg')

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quatity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

STATUS_CHOICES = (
    ('ACCEPTED','ACCEPTED'),
    ('PACKED','PACKED'),
    ('ON THE WAY','ON THE WAY'),
    ('DELIVERED','DELIVERED'),
    ('CANCEL','CANCEL')

)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
        















    
