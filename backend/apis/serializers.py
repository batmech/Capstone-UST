from rest_framework import serializers
from .models import Business, Users, Event, Review, Inventory, Messages, BusinessImages

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class EventSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.b_name', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'start_time', 'end_time', 'status', 'image', 'location', 'business_name', 'business']

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    business_name = serializers.CharField(source='business.b_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'rating', 'likes', 'created_at', 'user', 'user_name', 'business', 'business_name']

class InventorySerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.b_name', read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'product_name', 'description', 'quantity', 'price', 'date_added', 'image', 'business_name', 'business']

class MessagesSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    business_name = serializers.CharField(source='business.b_name', read_only=True)

    class Meta:
        model = Messages
        fields = ['id', 'content', 'date', 'is_read', 'user', 'user_name', 'business', 'business_name']

class BusinessImagesSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.b_name', read_only=True)

    class Meta:
        model = BusinessImages
        fields = ['id', 'image_1', 'image_2', 'image_3', 'image_4', 'business', 'business_name']


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'email', 'location', 'zipcode', 'is_business_owner', 'bio', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            location=validated_data.get('location', ''),
            zipcode=validated_data.get('zipcode', ''),  
            is_business_owner=validated_data.get('is_business_owner', False),
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        return user