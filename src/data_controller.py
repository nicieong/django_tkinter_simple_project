"""
CST8333 Programming Language Research Project
Practical Project Part 02
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is the view part of MVC model.
It handles user input and update the model/view accordingly.
"""


class TrafficDataController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def list_all_records(self):
        records = self.model.read_all()
        self.view.display_all(records)

    def show_records(self, *row_numbers):
        records = self.model.read_by_row_numbers(*row_numbers)
        self.view.display_records(records)

    def add_record(self, new_record):
        self.model.create(new_record)
        self.view.display_record(new_record)

    def edit_record(self, row_number, updated_record):
        self.model.update(row_number, updated_record)
        self.view.display_record(updated_record)

    def remove_record(self, row_number):
        self.model.delete(row_number)
        self.view.display_deleted_msg(row_number)
