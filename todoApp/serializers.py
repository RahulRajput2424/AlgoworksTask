
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from todoApp.models import User,ToDo, Comment, Reply
from django.contrib.auth import authenticate, login
class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    
    class Meta:
        model = User
        fields = ['email', 'mobileNumber', 'password', 'username']
    
    def create(self, validate_data):
        user = User(mobileNumber=validate_data['mobileNumber'],
        username=validate_data['username'],
        email=validate_data['email'],
        )
        user.set_password(validate_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['email','password']
    
    def validate_email(self, email):
        if not User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("User does not exists. You need to  signup.")
        return email

    def validate(self, validate_data):
        email = validate_data.get('email')
        password = validate_data.get('password')
        
        if email and password:
            user_obj = User.objects.get(email__iexact=email)
            username = user_obj.username
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or Password.")
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        validate_data["user"] = user
        return validate_data

class AddTodoSerializer(serializers.ModelSerializer):
	end_date = serializers.DateTimeField(input_formats=(['%d-%m-%Y']))
	class Meta:
		model = ToDo
		fields = '__all__'

class AddCommnetSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Comment
		fields = '__all__'

class ListTodoSerializer(serializers.ModelSerializer):
	status = serializers.CharField()
	user = serializers.CharField()

	class Meta:
		model = ToDo
		fields = ('name', 'end_date', 'status', 'user')

class AddReplySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Reply
		fields = '__all__'

