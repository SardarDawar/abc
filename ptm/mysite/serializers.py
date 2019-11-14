from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User




class childSerializer(serializers.ModelSerializer):
    class Meta:
        model = child
        fields = ("id","name", "classname","parent","Date_of_birth","Date_of_birth","image","approve","Father_id")
    

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profileModel
        fields = ("id","user", "contactNumber","Teacher_or_Parent",'approve')


class attendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = attendence
        fields = ("id","name", "parent","classname","Date",'Dropped_or_pickup','drop_time','pick_up_time')

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ("id","title","classname", "subject","Date",'files','update')


class child_storiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = child_stories
        fields = ("id","name","classname", "description","Date",'files')
    

class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ("id","name", "recipient_email","title",'subject','files','Date','approved')