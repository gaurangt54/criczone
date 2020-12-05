from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png",null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
       return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    CATEGORY = (
        ('Bats','Bats'),
        ('Balls','Balls'),
        ('Pads', 'Pads'),
        ('Gloves', 'Gloves'),
        ('Safety Equipments', 'Safety Equipments'),
        ('Kits', 'Kits'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
       return self.name


class Order(models.Model):

    STATUS = (
        ('Pending','Pending'),
        ('Out of Delivery','Out of Delivery'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=355, null=True)
    quantity = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    notes = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.customer.name + " (" + self.product.name + ")"

    def total(self):
        return int(self.product.price * self.quantity)


class Cart(models.Model):

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True)

    def __str__(self):
       return (self.customer.name + " (" + self.product.name + ")")

