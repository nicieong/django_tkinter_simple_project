"""
CST8333 Programming Language Research Project
Practical Project Part 02
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is the view part of MVC model.
It displays data to the user correspond to different situations.
"""


class TrafficDataView:
    def display_all(self, records):
        for record in records:
            print(vars(record))

    def display_record(self, record):
        if record:
            print(vars(record))
        else:
            print("Record not found.")

    def display_records(self, records):
        if records:
            for record in records:
                print(vars(record))
        else:
            print("No records found.")

    def display_deleted_msg(self, row_number):
        print(f"Record with id {row_number} deleted.")
