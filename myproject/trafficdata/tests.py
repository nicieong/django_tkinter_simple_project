"""
CST8333 Programming Language Research Project
Practical Project Part 03
Student Name: Ka Yan Ieong
Student No.: 041070033

This file is to have unit tests for the endpoints setup

Steps:
1. navigate to trafficdata app folder
2. python manage.py tests  (run this file)
"""


# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import DynamicTrafficVolume


class ReadTrafficVolumesTest(TestCase):
    def setUp(self):
        # Create sample data in the database
        DynamicTrafficVolume.objects.create(data={"Highway": "101", "Section": "1A", "Description": "Main road passing through downtown."})
        DynamicTrafficVolume.objects.create(data={"Highway": "102", "Section": "1B", "Description": "Secondary road with scenic views."})

    def test_read_volumes(self):
        """ Test that the volumes are read correctly """
        volumes = DynamicTrafficVolume.objects.all()
        self.assertEqual(volumes.count(), 2)
        first_volume = volumes.first()
        self.assertEqual(first_volume.data['Highway'], '101')
        self.assertEqual(first_volume.data['Description'], 'Main road passing through downtown.')
        print(f'test_read_volumes test is prepared by Ka Yan Ieong 041070033')


class EndpointTests(TestCase):
    def setUp(self):
        # Setup test data
        DynamicTrafficVolume.objects.create(data={"Highway": "101", "Section": "1A", "Description": "Main road."})
        DynamicTrafficVolume.objects.create(data={"Highway": "102", "Section": "1B", "Description": "Secondary road."})

    def test_get_traffic_volumes(self):
        # Get the URL using 'reverse' to ensure the test won't break if the URL changes
        url = reverse('trafficdata:api_volumes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Main road.", response.content.decode())  # Check if response data contains specific content
        print(f'test_get_traffic_volumes test is prepared by Ka Yan Ieong 041070033')

    def test_create_traffic_volume(self):
        url = reverse('trafficdata:create_volume')
        data = {
            "data": {
                "Highway": "103",
                "Section": "1C",
                "Description": "New road."
            }
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        print(f'test_create_traffic_volume test is prepared by Ka Yan Ieong 041070033')

    def test_update_traffic_volume(self):
        volume = DynamicTrafficVolume.objects.get(data__Section="1A")  # Use 'data__Section' to access the JSON key
        url = reverse('trafficdata:update_volume', args=[volume.id])
        new_data = {"data": {"Highway": "101", "Section": "1A", "Description": "Updated road."}}
        response = self.client.put(url, new_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Reloading volume from database to confirm updates
        volume.refresh_from_db()
        self.assertEqual(volume.data["Description"], "Updated road.")
        print(f'test_update_traffic_volume test is prepared by Ka Yan Ieong 041070033')

    def test_delete_traffic_volume(self):
        volume = DynamicTrafficVolume.objects.get(data__Section="1B")
        url = reverse('trafficdata:delete_volume', args=[volume.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(DynamicTrafficVolume.objects.count(), 1)
        print(f'test_delete_traffic_volume test is prepared by Ka Yan Ieong 041070033')

