"""
CST8333 Programming Language Research Project
Practical Project Part 03
Student Name: Ka Yan Ieong
Student No.: 041070033
"""

from rest_framework import serializers
from .models import DynamicTrafficVolume


class DynamicTrafficVolumeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DynamicTrafficVolume
        fields = '__all__'

    def create(self, validated_data):
        # Override create to handle JSON data formatting if necessary
        return DynamicTrafficVolume.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update instance according to the validated data
        instance.data = validated_data.get('data', instance.data)
        instance.save()
        return instance
