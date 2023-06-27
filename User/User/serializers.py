import re

from django.contrib.auth.models import User
from rest_framework import serializers
from User.models import ExtendedUser, Insurance


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    phoneNumber = serializers.CharField(write_only=True)

    class Meta:
        model = ExtendedUser
        fields = ['username', 'password', 'phoneNumber', ]

    def validate(self, attrs):
        if not re.match("09\\d{9}", attrs.get('phoneNumber', '')) or len(attrs.get('phoneNumber', '')) != 11:
            return serializers.ValidationError("Phone number must have 11 digits and starts with 09!")
        return attrs

    def create(self, validated_data):
        user = User()
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.save()
        extendedUser = ExtendedUser()
        extendedUser.user = user
        extendedUser.phoneNumber = validated_data['phoneNumber']
        extendedUser.save()
        return extendedUser


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = ExtendedUser
        fields = ['username', 'password', ]


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'


class InsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Insurance
        fields = '__all__'

    def validate(self, attrs):
        if not re.match("09\\d{9}", attrs.get('phoneNumber', '')) or len(attrs.get('phoneNumber', '')) != 11:
            return serializers.ValidationError("Phone number must have 11 digits and starts with 09!")
        if attrs.get('age', '') > 45:
            raise Exception("Age can't be more than 45!")
        if not attrs.get('BMISmooking', '') and attrs.get('smokingRatePerDay', '') != 0:
            raise Exception("Smoking BMI and smoking rate are not compatible!")
        if not attrs.get('BMIHookah', '') and attrs.get('hookahRatePerDay', '') != 0:
            raise Exception("hookah BMI and hookah rate are not compatible!")
        return attrs

    def create(self, validated_data):
        insurance = super().create(validated_data)
        insurance.save()
        request = self.context['request']
        theUser = None
        for user in ExtendedUser.objects.all():
            if user.user.username == request.user.username:
                theUser = user.user
                break
        theUser.insurance = insurance
        theUser.save()
        return insurance





