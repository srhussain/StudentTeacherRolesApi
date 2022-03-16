from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=('name',)

class StudentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentRecord
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    groups=GroupSerializer(many=True)
    studentrecord=serializers.SerializerMethodField(read_only=True)
    # studentRecord=StudentRecordSerializer()
    class Meta:
        model=User
        fields=['id','first_name','last_name','email','username','is_email_verified','phone_no','groups','studentrecord']

    def create(self,validated_data):
        user=User.objects.create(email=validated_data['email'],username=validated_data['username'],first_name=validated_data['first_name'],last_name=validated_data['last_name'],
        phone_no=validated_data['phone_no'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_studentrecord(self,obj):      
        try:
            record= StudentRecordSerializer(obj.studentrecord.all(),many=True).data
        except:
            record=False
        return record

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()


class StudentListSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=StudentRecord
        fields='__all__'

    def get_user(self,obj):
        user=obj.user
        serializer=UserSerializer(user,many=False)
        return serializer.data



    
