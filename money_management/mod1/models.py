

# Create your models here.
from django.db import models
# class UserProfile(models.Model): #ekekta class ekekta table
#     #id=models.IntegerField
#     fname=models.CharField(max_length=250)
#     lname=models.CharField(max_length=250)
#     email=models.CharField(max_length=100)
#     phone_num=models.IntegerField

#     def __str__(self):
#         return self.fname + ' ' + self.email

class UserProfile(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # You may want to store hashed passwords

    def __str__(self):
        return self.username




