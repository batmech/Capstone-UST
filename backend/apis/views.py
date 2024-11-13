from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Business, Users, Event, Review, Inventory, Messages, BusinessImages
from rest_framework.throttling import UserRateThrottle
from .serializers import (
    BusinessSerializer, UsersSerializer, EventSerializer, 
    ReviewSerializer, InventorySerializer, MessagesSerializer, 
    BusinessImagesSerializer,
    UserSignUpSerializer
)

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_authenticated

class IsBusinessOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_business_owner

class BusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    
    
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated()]  
        return super().get_permissions()  


class BusinessListCreateView(generics.ListCreateAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Business.objects.all()
        
        # Get category, address, zipcode, and b_name from query parameters
        category = self.request.query_params.get('category', None)
        address = self.request.query_params.get('address', None)
        zipcode = self.request.query_params.get('zipcode', None)
        b_name = self.request.query_params.get('b_name', None)

        # Apply filters based on query parameters
        if category:
            queryset = queryset.filter(category=category)
        if address:
            queryset = queryset.filter(address__icontains=address)  # Case-insensitive search
        if zipcode:
            queryset = queryset.filter(zipcode=zipcode)
        if b_name:
            queryset = queryset.filter(b_name__icontains=b_name)  # Case-insensitive search
        
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("You must be logged in to create a business.")


class BusinessOwnerView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter businesses based on the owner
        return Business.objects.filter(owner=self.request.user)


class UsersListCreateView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        business = self.request.query_params.get('business', None)
        status = self.request.query_params.get('status', None)

        if business and status:
            queryset = queryset.filter(business__id=business, status=status)
        elif business:
            queryset = queryset.filter(business__id=business)
        elif status:
            queryset = queryset.filter(status=status)

        return queryset


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        
        # Get query parameters
        business = self.request.query_params.get('business', None)
        rating = self.request.query_params.get('rating', None)
        user = self.request.query_params.get('user', None)

        # Apply filters based on query parameters
        if business:
            queryset = queryset.filter(business__id=business)
        if rating:
            queryset = queryset.filter(rating=rating)
        if user:
            queryset = queryset.filter(user__id=user)

        # Order by business and rating
        queryset = queryset.order_by('business', '-rating')
        
        return queryset

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get_queryset(self):
        queryset = Inventory.objects.all()
        business_id = self.request.query_params.get('business', None)

        if business_id:
            queryset = queryset.filter(business_id=business_id)

        return queryset

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


class HourlyRateThrottle(UserRateThrottle):
    rate = '3/h'  

    def allow_request(self, request, view):
        is_allowed = super().allow_request(request, view)
        
        if not is_allowed:  
            response = Response(
                {"message": "You have exceeded the number of allowed requests per hour."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )  
            return response
        return is_allowed


class UserSignUpView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSignUpSerializer
    throttle_classes = [HourlyRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "User created successfully!"},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [HourlyRateThrottle]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
  
            return Response({
                'userId': user.id,
                'username': user.username,
                'refresh': refresh_token,
                'is_business_owner': user.is_business_owner,
                'access': access_token,
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)