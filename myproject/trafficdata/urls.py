"""
CST8333 Programming Language Research Project
Practical Project Part 04
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is to define the endpoints and their names to be used in other parts of codes within the project
"""

from django.urls import path
from .views import TrafficVolumeListAPIView, TrafficVolumeDetailView, TrafficVolumeCreate, TrafficVolumeUpdate, \
    TrafficVolumeDelete, TrafficVolumeInitialAPIView, TrafficVolumeDetailBySectionIdByCountyByDirectionView

app_name = 'trafficdata'  # Define the application namespace here

urlpatterns = [
    path('api/volumes/', TrafficVolumeListAPIView.as_view(), name='api_volumes'),
    path('api/volumes/initial/', TrafficVolumeInitialAPIView.as_view(), name='initial_volumes'),
    path('api/volumes/<int:pk>/', TrafficVolumeDetailView.as_view(), name='volume-detail'),
    path('api/volumes/<str:section_id>/<str:type>/', TrafficVolumeDetailBySectionIdByCountyByDirectionView.as_view(),
         name='volume_detail_by_section_id_by_county_by_direction'),
    path('api/volumes/create/', TrafficVolumeCreate.as_view(), name='create_volume'),
    path('api/volumes/update/<int:pk>/', TrafficVolumeUpdate.as_view(), name='update_volume'),
    path('api/volumes/delete/<int:pk>/', TrafficVolumeDelete.as_view(), name='delete_volume'),
]
