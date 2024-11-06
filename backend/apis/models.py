import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

def inventory_image_distributor(instances, filename):
     return os.path.join('business', f'{instances.business.b_name}', f'{instances.business.id}', 'products', filename)

def default_work_time():
    return {
        "Monday": {"open": "09:00", "close": "17:00"},
        "Tuesday": {"open": "09:00", "close": "17:00"},
        "Wednesday": {"open": "09:00", "close": "17:00"},
        "Thursday": {"open": "09:00", "close": "17:00"},
        "Friday": {"open": "09:00", "close": "17:00"},
        "Saturday": {"open": "10:00", "close": "15:00"},
        "Sunday": {"open": "Closed", "close": "Closed"},
    }

def business_image_upload_to(instance, filename):
    business_id = str(instance.business.id)
    if isinstance(instance, BusinessImages):
        return os.path.join('business', business_id, 'optional', filename)
    elif isinstance(instance, Business):
        return os.path.join('business', business_id, 'main', filename)
            

class Event(models.Model):
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='business_events')
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published'), ('cancelled', 'Cancelled')])
    image = models.ImageField(upload_to='eventImages')
    location = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.business.b_name}"

class BusinessImages(models.Model):
    business = models.ForeignKey("Business", on_delete=models.CASCADE, related_name='business_image_set')
    image_1 = models.ImageField(upload_to=business_image_upload_to, null=True, blank=True)
    image_2 = models.ImageField(upload_to=business_image_upload_to, null=True, blank=True)
    image_3 = models.ImageField(upload_to=business_image_upload_to, null=True, blank=True)
    image_4 = models.ImageField(upload_to=business_image_upload_to, null=True, blank=True)

    def __str__(self):
        return f"Images for {self.business.b_name} (Main: {self.main_image.name})"

class Users(AbstractUser):
    location = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    is_business_owner = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/')
    last_login = models.DateTimeField(auto_now=True)  

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.last_login = timezone.now()  
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username

class Business(models.Model):
    CATEGORY_CHOICES = [
        ('RESTAURANT', 'Restaurant'),
        ('BOOKSTORE', 'Bookstore'),
        ('SALON', 'Salon'),
        ('SUPERMARKET', 'Supermarket'),
    ]
    
    b_name = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    address = models.TextField()
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    website = models.CharField(max_length=254, blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_registered = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to=business_image_upload_to)
    work_time = models.JSONField(blank=False, default=default_work_time)
    
    def __str__(self):
        return f"{self.b_name} - {self.owner} ({self.category})"
    

class Inventory(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=inventory_image_distributor)
    
    def __str__(self):
        return self.product_name

class Messages(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    

class Review(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])    
    likes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
