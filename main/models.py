from django.db import models


class Order(models.Model):
    order_id = models.IntegerField()
    email = models.CharField()
    phone_number = models.CharField()
    bot_shop = models.IntegerField()
    admin_panel = models.IntegerField()
    database = models.IntegerField()
    total_price = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'order'


class Product(models.Model):
    product = models.CharField()
    price = models.IntegerField()
    title = models.CharField()

    class Meta:
        db_table = 'product'


class User(models.Model):
    phone_number = models.CharField()
    email = models.CharField()
    hashed_password = models.CharField(max_length=1024)
    registered = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField()
    is_superuser = models.BooleanField()
    is_verified = models.BooleanField()

    class Meta:
        db_table = 'user'
