from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, status, permissions
from .models import Business, Users, Event, Review, Inventory, Messages, BusinessImages
from .serializers import (
    BusinessSerializer, UsersSerializer, EventSerializer, 
    ReviewSerializer, InventorySerializer, MessagesSerializer, 
    BusinessImagesSerializer
)
from .permissions import IsBusinessOwner

class BusinessListCreateView(generics.ListCreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.username)

class BusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    # permission_classes = [permissions.IsAuthenticated, IsBusinessOwner] 
    permission_classes = [IsBusinessOwner] 

class UsersListCreateView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class MessagesListCreateView(generics.ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

class MessagesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

class BusinessImagesListCreateView(generics.ListCreateAPIView):
    queryset = BusinessImages.objects.all()
    serializer_class = BusinessImagesSerializer

class BusinessImagesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessImages.objects.all()
    serializer_class = BusinessImagesSerializer
