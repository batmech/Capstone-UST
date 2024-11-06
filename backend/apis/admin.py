from django.contrib import admin
from .models import Business, Users, Event, Review, Inventory, Messages, BusinessImages

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['b_name', 'owner', 'category', 'phone', 'email', 'date_registered']
    search_fields = ['b_name', 'owner', 'category', 'phone']
    list_filter = ['category', 'date_registered']
    ordering = ['date_registered']

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'location', 'is_business_owner', 'date_joined']
    search_fields = ['username', 'email', 'location']
    list_filter = ['is_business_owner', 'date_joined']
    ordering = ['date_joined']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'start_time', 'end_time', 'status', 'location']
    search_fields = ['name', 'business__b_name', 'status', 'location']
    list_filter = ['status', 'start_time', 'end_time']
    ordering = ['start_time']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['business', 'user', 'title', 'rating', 'likes', 'created_at']
    search_fields = ['title', 'business__b_name', 'user__username']
    list_filter = ['rating', 'created_at']
    ordering = ['created_at']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['business', 'product_name', 'quantity', 'price', 'date_added']
    search_fields = ['product_name', 'business__b_name']
    list_filter = ['date_added']
    ordering = ['date_added']

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['business', 'user', 'content', 'date', 'is_read']
    search_fields = ['business__b_name', 'user__username', 'content']
    list_filter = ['is_read', 'date']
    ordering = ['date']

@admin.register(BusinessImages)
class BusinessImagesAdmin(admin.ModelAdmin):
    list_display = ['business', 'image_1', 'image_2', 'image_3', 'image_4']
    search_fields = ['business__b_name']
