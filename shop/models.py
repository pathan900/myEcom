from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=300)
    product_desc = models.CharField(max_length=1000)
    price = models.IntegerField(default=0)
    pub_date = models.DateField()
    category = models.CharField(max_length=100, default='')
    subcategory = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='shop/images', default='')

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    country = models.CharField(max_length=25)
    subject = models.CharField(max_length=500, default='')
    dsc = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=150, default='')
    mobile = models.IntegerField(default=0)
    email = models.CharField(max_length=500, default='')
    address = models.CharField(max_length=1000, default='')
    landmark = models.CharField(max_length=600, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    zip_code = models.IntegerField(default=0)

    def __int__(self):
        return self.order_id


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default='')
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "...."





















