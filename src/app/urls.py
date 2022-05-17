from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app import views
from knox import views as knox_views

router = DefaultRouter()

# empty path URL first throwing detail not found, so keep router with the empty path at last
router.register('movie', views.MovieViewSet, basename='movie')
router.register('actor', views.ArtistViewSet, basename='actor')


urlpatterns = [
    path('app/', include(router.urls)),
    path('user/register/', views.SignUpAPI.as_view(), name='register'),
    path('user/login/', views.LoginView.as_view(), name='knox_login'),
    path('user/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('booking/<str:movie>/', views.BookingAPIView.as_view(), name="ticket"),
    path('bulkupdate/', views.BulkAPIView.as_view(), name='bulk'),
]
