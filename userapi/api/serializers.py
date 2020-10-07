from rest_framework import serializers
from userapi.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    class Meta:

        model = User
        fields = ('first_name','last_name','username','email','role','password')
    
    def create(self,validated_data): 
        password = validated_data.get('password',None)
        data = validated_data
        instance = User(**data)
        if password:   
          instance.set_password(password)
        instance.save()
        return instance

