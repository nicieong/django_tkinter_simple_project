"""
CST8333 Programming Language Research Project
Practical Project Part 03
Student Name: Ka Yan Ieong
Student No.: 041070033
"""

# Create your models here.
from django.db import models
import json


class DynamicTrafficVolume(models.Model):
    data = models.JSONField(help_text="Stores row data as JSON.")  # Use Django's native JSONField

    def get_data(self):
        try:
            return json.loads(self.data)
        except json.JSONDecodeError:
            return {}  # Return an empty dict if there's an error in decoding

    def set_data(self, data):
        self.data = json.dumps(data)  # Convert dictionary to a JSON string