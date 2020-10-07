from django.db import models
from  django.contrib.auth.models import User as DjangoUser

class User(DjangoUser):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT ='student'
    
    ROLE_CHOICES = (
          (ADMIN,'admin'),
          (TEACHER, 'teacher'),
          (STUDENT, 'student'),
          
      )
    role = models.CharField(max_length=100,choices=ROLE_CHOICES, blank=True, null=True)