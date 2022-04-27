from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app import views
from knox import views as knox_views

router = DefaultRouter()
routers1 = DefaultRouter()

# empty path URL first and throwing detail not found, so keep router with the empty path at last
routers1.register('update', views.UpdateViewSet, basename='update')
routers1.register('artist', views.ArtistViewSet, basename='artist')
routers1.register('ticket', views.TicketViewSet, basename='seat')
router.register('', views.ActorViewSet, basename='actor')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/<str:bk>/<str:ck>/', include(router.urls)),
    path('app/', include(routers1.urls)),
    path('bulk/', views.BulkAPIView.as_view(), name='bulk'),
    path('register/', views.SignUpAPI.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]
