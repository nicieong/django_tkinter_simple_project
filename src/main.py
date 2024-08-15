"""
CST8333 Programming Language Research Project
Practical Project Part 01
Student Name: Ka Yan Ieong
Student No.: 041070033

This file is to run the main program to trigger CRUD operations.
Functions details are implemented in other py files
"""

import data_model, data_view, data_controller


def main():
    file_path = r'C:/Users/kyieo/PycharmProjects/CST8333/src/Traffic_Volumes_-_Provincial_Highway_System.csv'
    target_file_path = r'C:/Users/kyieo/PycharmProjects/CST8333/src/first_hundred_records.csv'

    all_objects_list = data_model.parse_csv_to_objects(file_path)

    # write first 100 records to a new CSV file
    # the remain operations will access data from the new CSV file
    data_model.write_first_hundred_records(all_objects_list, target_file_path)

    model = data_model.TrafficDataModel(target_file_path)
    view = data_view.TrafficDataView()
    controller = data_controller.TrafficDataController(model, view)

    # Access Controller to List all records
    print("All records:")
    controller.list_all_records()

    # show the size of the in memory list to check if the memory list is correctly modified
    # not part of the MVC model. it is just a crosscheck log message
    print(data_model.TrafficDataModel.size_of_objects_list())

    # ready a new record
    new_record_values = {
        'SECTION ID': '10000',
        'HIGHWAY': '10000',
        'SECTION': '10000',
    }

    # Access Controller to Add a new record
    new_record = data_model.TrafficVolumesData(model.read_headers(), new_record_values)
    print("\nAdding a new record:")
    controller.add_record(new_record)

    # show the size of the in memory list to check if the memory list is correctly modified
    # not part of the MVC model. it is just a crosscheck log message
    print(data_model.TrafficDataModel.size_of_objects_list())

    # Access Controller to Show a specific record
    print("\nShowing record with row number 2:")
    controller.show_records('2')

    # Access Controller to Show a number of specific records
    print("\nShowing record with row number 1, 2, 3:")
    controller.show_records('1', '2', '3')

    # ready a record to update
    update_record_values = {
        'SECTION ID': '99999',
        'HIGHWAY': '99999',
        'SECTION': '99999'
    }

    # turn the record to be updated as a Traffic Volume Data object
    updated_record = data_model.TrafficVolumesData(model.read_headers(), update_record_values)
    # instruct to update the last record
    last_record = data_model.TrafficDataModel.size_of_objects_list()

    # Access Controller to Update a specific record
    print(f"\nUpdating record with row number {last_record}:")
    controller.edit_record(last_record, updated_record)

    # show the size of the in memory list to check if the memory list is correctly modified
    # not part of the MVC model. it is just a crosscheck log message
    print(data_model.TrafficDataModel.size_of_objects_list())

    # Access Controller to Delete a record
    print(f"\nDeleting record with row number {last_record}:")
    controller.remove_record(last_record)  # delete last record

    # show the size of the in memory list to check if the memory list is correctly modified
    # not part of the MVC model. it is just a crosscheck log message
    print(data_model.TrafficDataModel.size_of_objects_list())

    # Access Controller to Show a number of specific records
    print("\nShowing record of first 5 rows:")
    controller.show_records('1', '2', '3', '4', '5')

    print("Works done by Ka Yan Ieong - 041070033")


# ensures the script runs only when executed directly, not when imported as a module
if __name__ == "__main__":
    main()
