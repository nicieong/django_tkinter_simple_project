"""
CST8333 Programming Language Research Project
Practical Project Part 03
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is part of the Django framework
It is under the app trafficdata directory
The file is loading to Django database (sqlite)

It is a command line enabled script
Backend will run the script to load the first hundred record Django database (sqlite)
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
import csv
import os
from pathlib import Path
from trafficdata.models import DynamicTrafficVolume


class Command(BaseCommand):
    help = 'Load traffic data from CSV into the Django model and reset IDs'

    def handle(self, *args, **options):
        # Clear existing records
        DynamicTrafficVolume.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing records.'))

        # Reset the primary key sequence
        self.reset_auto_increment()

        # Load new data from CSV
        csv_file_path = os.path.join(settings.DATA_DIR, 'first_hundred_records.csv')
        if not Path(csv_file_path).exists():
            self.stdout.write(self.style.ERROR(f"CSV file {csv_file_path} does not exist"))
            return

        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            objects = [DynamicTrafficVolume(data=row) for row in reader]
            DynamicTrafficVolume.objects.bulk_create(objects)  # Using bulk_create for efficiency

        self.stdout.write(self.style.SUCCESS('Successfully loaded CSV data into Django.'))

    def reset_auto_increment(self):
        if connection.vendor == 'postgresql':
            with connection.cursor() as cursor:
                cursor.execute("ALTER SEQUENCE trafficdata_dynamictrafficvolume_id_seq RESTART WITH 1;")
                self.stdout.write(self.style.SUCCESS('Reset PostgreSQL sequence.'))
        elif connection.vendor == 'sqlite':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='trafficdata_dynamictrafficvolume';")
                self.stdout.write(self.style.SUCCESS('Reset SQLite autoincrement.'))
        elif connection.vendor == 'mysql':
            with connection.cursor() as cursor:
                cursor.execute("ALTER TABLE trafficdata_dynamictrafficvolume AUTO_INCREMENT = 1;")
                self.stdout.write(self.style.SUCCESS('Reset MySQL auto-increment.'))
        else:
            self.stdout.write(self.style.ERROR('Database vendor not supported for auto-increment reset.'))
