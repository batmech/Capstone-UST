from rest_framework import serializers
from .models import Business, Users, Event, Review, Inventory, Messages, BusinessImages

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

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
        fields = ['id', 'main_image', 'image_1', 'image_2', 'image_3', 'image_4', 'business', 'business_name']
