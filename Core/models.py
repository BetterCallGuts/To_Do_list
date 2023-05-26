from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


USer = get_user_model()

'''

Create your models here.

'''
class Account(models.Model):
    user = models.ForeignKey(USer, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)+ str(self.user.username)



class ToDoTask(models.Model):
    user = models.ForeignKey(Account , on_delete=models.CASCADE)
    Title = models.CharField(max_length=50)
    Created_at = models.DateTimeField(default=datetime.now)
    description = models.CharField(max_length=250)




    def __str__(self):
        return self.user