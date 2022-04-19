from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from app import views



router = DefaultRouter()
app_name = 'app'


#empty path URL first and throwing detail not found, so keep router with the empty path at last
router.register('update', views.UpdateViewSet,basename='update')
router.register('artist', views.ArtistViewSet,basename='artist')
router.register('city', views.CityViewSet,basename='cities-detail')
router.register('ac', views.AcViewSet,basename='ac')
router.register('', views.ActorViewSet,basename='actor')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/<str:bk>/', include(router.urls)),
]
