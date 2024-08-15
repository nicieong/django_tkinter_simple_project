"""
CST8333 Programming Language Research Project
Practical Project Part 03
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is part of the Django framework
It is under the app trafficdata directory
The file is for importing the original dataset to Django framework
and write a first hundred record csv file for loading to Django database (sqlite)

It is a command line enabled script
Backend will run the script to first load the dataset
"""

from django.core.management.base import BaseCommand, CommandError
import csv
from pathlib import Path
from django.conf import settings
import os

class TrafficVolumesData:
    def __init__(self, headers, initial_values=None):
        initial_values = initial_values or {}
        for header, value in initial_values.items():
            setattr(self, header.lower().replace(' ', '_'), value)
        for header in headers:
            if not hasattr(self, header.lower().replace(' ', '_')):
                setattr(self, header.lower().replace(' ', '_'), None)

class Command(BaseCommand):
    help = 'Imports traffic data from a CSV and writes the first 100 records to another CSV'

    def handle(self, *args, **options):
        source_file_path = os.path.join(settings.DATA_DIR, 'Traffic_Volumes_-_Provincial_Highway_System.csv')
        target_file_path = os.path.join(settings.DATA_DIR, 'first_hundred_records.csv')

        if not Path(source_file_path).exists():
            raise CommandError(f"Error: File '{source_file_path}' not found.")

        headers, objects_list = self.parse_csv_to_objects(source_file_path)

        if objects_list:
            self.write_first_hundred_records(objects_list, target_file_path, headers)
            self.stdout.write(self.style.SUCCESS('Successfully processed and saved first 100 records.'))
        else:
            self.stdout.write('No data to process.')

    def parse_csv_to_objects(self, file_path):
        try:
            with open(file_path, 'r', newline='') as file:
                csv_reader = csv.DictReader(file)
                objects_list = [TrafficVolumesData(csv_reader.fieldnames, row) for row in csv_reader]
            return csv_reader.fieldnames, objects_list
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")

    def write_first_hundred_records(self, objects_list, target_file_path, headers):
        try:
            with open(target_file_path, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([header.lower().replace(' ', '_') for header in headers])
                for obj in objects_list[:100]:
                    row = [getattr(obj, header.lower().replace(' ', '_')) for header in headers]
                    csv_writer.writerow(row)
        except Exception as e:
            raise CommandError(f"An error occurred when writing to file: {e}")
