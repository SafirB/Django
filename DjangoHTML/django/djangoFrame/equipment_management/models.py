from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.shortcuts import render
from django.conf import settings



# Model for the actual equipment items
class Item(models.Model):
    item_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    serial = models.CharField(max_length=255, blank=True, null=True)
    cpu = models.CharField(max_length=255, blank=True, null=True)
    gpu = models.CharField(max_length=255, blank=True, null=True)
    ram = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'item_item'  # This tells Django which table to use

    def __str__(self):
        return self.name
    


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )
    
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Reservation by {self.user.username} for {self.item.name} on {self.date} at {self.time}'

    def get_absolute_url(self):
        # Redirect to the reservation detail page after creating a reservation
        return reverse('reservation-detail', kwargs={'pk': self.pk})


class Product(models.Model):
    name = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)  # Indicates if the product is available for reservation

    def __str__(self):
        return self.name
    

