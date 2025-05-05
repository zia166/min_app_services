from django.urls import path
from .import views
from .views import my_view
from rest_framework.urlpatterns import format_suffix_patterns
EventViewSet = views.EventViewSet()
urlpatterns = [
     path('my-view/', my_view, name='my_view'),
     path('events/', EventViewSet.eventOp, name='events'),
     path('user_details/<str:email>/', EventViewSet.userDetails, name='user_details'),
     path('event_details/', EventViewSet.eventDetails, name='event_details'),

]
urlpatterns = format_suffix_patterns(urlpatterns)