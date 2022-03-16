from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager



    
# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=20,unique=True)
    email=models.EmailField(unique=True)
    is_email_verified=models.BooleanField(default=False)
    phone_no=models.CharField(max_length=10,unique=True,null=True,blank=True)


    


    # USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email']
    objects=UserManager()


    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.username


class StudentRecord(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    student_name=models.CharField(max_length=15)
    student_class=models.CharField(max_length=100)
    student_rollno=models.CharField(max_length=20)
    student_marks=models.IntegerField(null=True,blank=True)

    def __str__(self) -> str:
        return self.user.username




