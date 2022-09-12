from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=40, null=False)
    birthday = models.DateField(null=False)
    email = models.EmailField(max_length=50, unique=True, null=False)
    address = models.CharField(max_length=50)
    updated_at = models.DateField(null=False, auto_now=True)
    created_at = models.DateField(null=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']


class ContactPhone(models.Model):
    phone = models.CharField(max_length=13, unique=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    updated_at = models.DateField(null=False, auto_now=True)
    
    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'
        ordering = ['-updated_at']