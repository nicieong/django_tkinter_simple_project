"""
CST8333 Programming Language Research Project
Practical Project Part 04
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is to define operations of the endpoints
The details are mapped by classes and point to urls.py
The Swagger documentation descriptions are also added here
Users can read the REST documentation from the setup here
"""

# Create your views here.
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DynamicTrafficVolume
from .serializers import DynamicTrafficVolumeSerializer


def home(request):
    return HttpResponse("Welcome to the Traffic Data App!")


# Get method for loading all data
class TrafficVolumeListAPIView(APIView):
    @swagger_auto_schema(
        responses={200: DynamicTrafficVolumeSerializer(many=True)},
        operation_description="Retrieve a list of all traffic volumes"
    )
    def get(self, request):
        volumes = DynamicTrafficVolume.objects.all()
        serializer = DynamicTrafficVolumeSerializer(volumes, many=True)
        return Response(serializer.data)


# Get method for loading initial 5 records
class TrafficVolumeInitialAPIView(APIView):
    @swagger_auto_schema(
        responses={200: DynamicTrafficVolumeSerializer(many=True)},
        operation_description="Retrieve initial set of 5 traffic volumes"
    )
    def get(self, request):
        volumes = DynamicTrafficVolume.objects.all()[:5]
        serializer = DynamicTrafficVolumeSerializer(volumes, many=True)
        return Response(serializer.data)


# Get method for loading specific record from the dataset
class TrafficVolumeDetailView(APIView):
    @swagger_auto_schema(
        responses={200: DynamicTrafficVolumeSerializer()},
        operation_id='get_single_volume',
        operation_description="Retrieve a specific traffic volume by its ID"
    )
    def get(self, request, pk):
        volume = get_object_or_404(DynamicTrafficVolume, pk=pk)
        serializer = DynamicTrafficVolumeSerializer(volume)
        return Response(serializer.data)


# Get method for loading records by 3 parameters: Section ID, County, and Direction at the same time
# Section ID and County are mandatory, direction is optional
class TrafficVolumeDetailBySectionIdByCountyByDirectionView(APIView):
    # Get method for loading records by 3 parameters: Section ID, County, and Direction at the same time
    # Section ID and County are mandatory, direction is optional
    @swagger_auto_schema(
        operation_id='get_volume_by_section_and_type_optional_direction',
        manual_parameters=[
            openapi.Parameter('section_id', openapi.IN_PATH, description="ID of the section",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_PATH, description="Type of the volume", type=openapi.TYPE_STRING),
            openapi.Parameter('direction', openapi.IN_QUERY, description="Direction of the traffic volume",
                              type=openapi.TYPE_STRING, required=False)
        ],
        responses={200: DynamicTrafficVolumeSerializer(many=True), 404: 'Not Found'}
    )
    def get(self, request, section_id, type):
        direction = request.query_params.get('direction', None)
        query = {'data__section_id': section_id, 'data__type': type}
        if direction is not None:
            query['data__direction'] = direction

        volumes = DynamicTrafficVolume.objects.filter(**query)
        if not volumes.exists():
            return Response({'message': 'No matching volumes found.'}, status=404)

        serializer = DynamicTrafficVolumeSerializer(volumes, many=True)
        return Response(serializer.data)


# Post method to insert a record to the dataset
class TrafficVolumeCreate(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'dynamicData': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=openapi.Schema(type=openapi.TYPE_STRING),
                description="Dynamic key-value pairs, where both keys and values are strings."
            )
        },
        description="A JSON object with dynamic keys and string values."
    ))
    def post(self, request):
        serializer = DynamicTrafficVolumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Put method to update an existing record
class TrafficVolumeUpdate(APIView):
    @swagger_auto_schema(
        request_body=DynamicTrafficVolumeSerializer,
        responses={200: DynamicTrafficVolumeSerializer()},
        operation_description="Update an existing traffic volume by its ID"
    )
    def put(self, request, pk):
        volume = get_object_or_404(DynamicTrafficVolume, pk=pk)
        serializer = DynamicTrafficVolumeSerializer(volume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete method to remove an existing record
class TrafficVolumeDelete(APIView):
    @swagger_auto_schema(
        responses={204: 'Successfully deleted.'},
        operation_description="Delete a traffic volume by its ID"
    )
    def delete(self, request, pk):
        volume = get_object_or_404(DynamicTrafficVolume, pk=pk)
        volume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
