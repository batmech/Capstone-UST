from django.urls import path
from .views import (
    BusinessListCreateView, BusinessDetailView,
    UsersListCreateView, UsersDetailView,
    EventListCreateView, EventDetailView,
    ReviewListCreateView, ReviewDetailView,
    InventoryListCreateView, InventoryDetailView,
    MessagesListCreateView, MessagesDetailView,
    BusinessImagesListCreateView, BusinessImagesDetailView,
    UserSignUpView,
    LoginView,
    BusinessOwnerView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('businesses/', BusinessListCreateView.as_view(), name='business-list-create'),
    path('businesses/<int:pk>/', BusinessDetailView.as_view(), name='business-detail'),
    path('businesses/owner/', BusinessOwnerView.as_view(), name='business-owner-list'),

    path('users/', UsersListCreateView.as_view(), name='users-list-create'),
    path('users/<int:pk>/', UsersDetailView.as_view(), name='users-detail'),

    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    path('inventory/', InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),

    path('messages/', MessagesListCreateView.as_view(), name='messages-list-create'),
    path('messages/<int:pk>/', MessagesDetailView.as_view(), name='messages-detail'),

    path('business-images/', BusinessImagesListCreateView.as_view(), name='business-images-list-create'),
    path('business-images/<int:pk>/', BusinessImagesDetailView.as_view(), name='business-images-detail'),
    
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('signup/', UserSignUpView.as_view(), name='user_signup'),
    path('login/', LoginView.as_view(), name='user_login'),

]
