"""
CST8333 Programming Language Research Project
Practical Project Part 02
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is for initial file handling
such as read entire dataset
and write first 100 records to a new file.

This py file is also the model part of MVC model.
It handles reading from and writing to the CSV file.
It includes methods for CRUD operations.
"""

import csv


# declare a class with the dynamic attributes assigned based on the info in dataset
# avoid hard code for easier codebase maintenance
class TrafficVolumesData:
    def __init__(self, headers, initial_values=None):
        initial_values = initial_values or {}
        for header, value in initial_values.items():
            setattr(self, header.lower().replace(' ', '_'), value)
        for header in headers:
            if not hasattr(self, header.lower().replace(' ', '_')):
                setattr(self, header.lower().replace(' ', '_'), None)


# read headers from the dataset
def read_headers(file_path):
    try:
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            return headers

    # handle file not found error
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

    # handle file permission error
    except PermissionError:
        print(f"Error: Permission denied to open '{file_path}'.")

    # catch other unexpected errors
    except Exception as exception:
        print(f"An error occurred: {exception}")


# load the data in csv file and parse them into class attributes and objects accordingly
def parse_csv_to_objects(file_path):
    # Read headers from the CSV file
    headers = read_headers(file_path)
    objects_list = []

    try:
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Create a dictionary to hold initial values for the TrafficVolumesData instance
                initial_values = {header: row.get(header, None) for header in headers}
                # Create an instance of TrafficVolumesData and append it to the list
                objects_list.append(TrafficVolumesData(headers, initial_values))

    # handle file not found error
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

    # handle file permission error
    except PermissionError:
        print(f"Error: Permission denied to open '{file_path}'.")

    # catch other unexpected errors
    except Exception as exception:
        print(f"An error occurred: {exception}")

    return objects_list


def write_first_hundred_records(objects_list, target_file_path):
    if not objects_list:
        print("No data to write.")
        return

    # read the headers from the original file
    headers = [header.lower().replace(' ', '_') for header in objects_list[0].__dict__.keys()]

    try:
        # instruct the program to write a CSV file
        with open(target_file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(headers)

            # limit to first 100 records only
            for obj in objects_list[:100]:
                row = [getattr(obj, header) for header in headers]
                csv_writer.writerow(row)

    # handle file not found error
    except FileNotFoundError:
        print(f"Error: File '{target_file_path}' not found.")

    # handle file permission error
    except PermissionError:
        print(f"Error: Permission denied to open '{target_file_path}'.")

    # catch other unexpected errors
    except Exception as exception:
        print(f"An error occurred: {exception}")


# define the model and CRUD operations
class TrafficDataModel:
    # for in-memory list storage
    objects_list = []

    def __init__(self, file_path):
        self.file_path = file_path

    @classmethod
    def size_of_objects_list(cls):
        return len(cls.objects_list)

    def read_headers(self):
        return read_headers(self.file_path)

    def read_all(self):
        headers = self.read_headers()
        if self.size_of_objects_list() > 0:
            data = self.objects_list
        else:
            data = []
            try:
                with open(self.file_path, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        data.append(TrafficVolumesData(headers, row))
                TrafficDataModel.objects_list = data
            # handle file not found error
            except FileNotFoundError:
                print(f"Error: File '{self.file_path}' not found.")

            # handle file permission error
            except PermissionError:
                print(f"Error: Permission denied to open '{self.file_path}'.")

            # catch other unexpected errors
            except Exception as exception:
                print(f"An error occurred: {exception}")
        return data

    def create(self, new_record):
        self.objects_list.append(new_record)

    def read_by_row_numbers(self, *row_numbers):
        data = self.objects_list
        results = []
        for row_number in row_numbers:
            row_number = int(row_number) - 1  # Convert row_number to integer & start the row_number at 1
            if 0 <= row_number < len(data):
                results.append(data[row_number])
        return results

    def update(self, row_number, updated_record):
        data = self.objects_list
        for row in enumerate(data):
            row_number = int(row_number) - 1  # Convert row_number to integer & start the row_number at 1
            if 0 <= row_number < len(data):
                data[row_number] = updated_record
                TrafficDataModel.objects_list = data  # Append to object list
                return
        raise ValueError(f"Record with id {row_number} not found")

    def delete(self, row_number):
        data = self.objects_list
        row_number = int(row_number) - 1  # Convert row_number to integer & start the row_number at 1
        if 0 <= row_number < len(data):
            del data[row_number]
            TrafficDataModel.objects_list = data  # Append to object list
            return
        raise ValueError(f"Record with id {row_number} not found")
