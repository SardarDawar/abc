from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

CHOICES_TYPE = (
    ('Teacher', 'Teacher'),
    ('Parent', 'Parent')
)
choices1 = (('Sick Leave','Sick Leave'),('Holiday','Holiday'),)



class profileModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    contactNumber = models.IntegerField(blank = True, null=True)
    approve = models.BooleanField(default=False)
    Teacher_or_Parent = models.CharField(max_length=10, blank=False, default='Teacher' ,choices=CHOICES_TYPE)
    
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User , on_delete= models.CASCADE)

    def __str__(self):
        return self.name


class child(models.Model):
    name             = models.CharField(max_length=100)
    classname        = models.ForeignKey(Class , on_delete= models.CASCADE)
    parent           = models.ForeignKey(User , on_delete= models.CASCADE)
    Date_of_birth    = models.DateField()
    image            = models.ImageField(blank=True)
    approve          = models.BooleanField(default=False,blank=True)
    Father_id        = models.CharField(max_length=100)

    def __str__(self):
         return self.name

class attendence(models.Model):
    name             = models.CharField(max_length=100)
    parent           = models.ForeignKey(User , on_delete= models.CASCADE)
    classname        = models.ForeignKey(Class , on_delete= models.CASCADE)
    Date             = models.DateTimeField(auto_now_add=True)
    Dropped_or_pickup   = models.BooleanField(default=False,blank=True)
    drop_time        = models.DateTimeField(auto_now_add=True)
    pick_up_time      = models.DateTimeField(auto_now=True)


class Notifications(models.Model):
    title             = models.CharField(max_length=100)
    subject           = models.TextField(max_length=1000)
    files             = models.FileField(blank=True)
    classname         = models.ForeignKey(Class , on_delete= models.CASCADE)
    Date              = models.DateTimeField(auto_now_add=True)
    update            = models.CharField(max_length=100, blank=True)


class child_stories(models.Model):
    name              = models.ForeignKey(child , on_delete= models.CASCADE)
    description       = models.CharField(max_length=1000)
    files             = models.FileField(blank=True)
    classname         = models.ForeignKey(Class , on_delete= models.CASCADE)
    Date              = models.DateTimeField(auto_now_add=True)

class Leaves(models.Model):
    name              = models.ForeignKey(User , on_delete= models.CASCADE)
    recipient_email   = models.EmailField()
    title             = models.CharField(max_length=100)
    type_of_application=models.CharField(max_length=100,choices=choices1)
    subject           = models.TextField(max_length=1000)
    files             = models.FileField(blank=True)
    Date              = models.DateTimeField(auto_now_add=True)
    approved          = models.BooleanField(default=False,blank=True)

