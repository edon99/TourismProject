
from django.urls import include, path
from . import views as view


urlpatterns = [
    path('', view.home , name='site-home'),
    path('login/', view.user_login , name='login'),
    path('logout/',  view.logout_user, name='logout'),
    path('signup/',  view.signup, name='signup'),
    path('locations/',  view.locations, name='locations'),
    path('new-location/',  view.newLocation, name='new-location'),
    path('locations/<int:pk>',  view.locationDetails, name='location-details'),
    path('locations/<int:pk>/rating',  view.locationRating, name='location-rating'),
    path('get-verified/',  view.getVerified, name='get-verified'),
    path('profile/<int:pk>',  view.profile, name='profile'),
    # path('api/', view.LocationAPI, name='api'),
    
]