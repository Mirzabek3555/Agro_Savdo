from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class CropType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CropImage(models.Model):
    crop_type = models.ForeignKey(
            CropType,
            on_delete=models.CASCADE,
            related_name='images',
    )
    image = models.ImageField(upload_to='crops/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class FarmerCrop(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crops')
    crop_type = models.ForeignKey(CropType, on_delete=models.CASCADE, related_name='farmer_crops')
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    available_from = models.DateField()
    available_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.crop_type.name} by {self.farmer.username}'


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    crops_grown = models.ManyToManyField('CropType')

    def __str__(self):
        return self.user.username


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    interested_crops = models.ManyToManyField('CropType')

    def __str__(self):
        return self.user.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    farmer_crop = models.ForeignKey(FarmerCrop, on_delete=models.CASCADE)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity_kg * self.farmer_crop.price_per_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.id}'


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self): 
        return 


class CropCalendar(models.Model):
    crop_name = models.CharField(max_length=255)
    planting_start = models.DateField()
    planting_end = models.DateField()
    harvesting_start = models.DateField()
    harvesting_end = models.DateField()
    region = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.crop_name} ({self.region})'


