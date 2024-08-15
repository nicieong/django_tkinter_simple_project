"""
CST8333 Programming Language Research Project
Practical Project Part 04
Student Name: Ka Yan Ieong
Student No.: 041070033

This py file is the GUI set up for users to interact with the dataset
such as doing CRUD operations and reload the dataset to the GUI interface
"""

import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
import requests
import subprocess

class TrafficVolumeApp:
    def __init__(self, root):  # Initialize the application with the root window
        self.root = root
        self.root.title("Traffic Volume App")  # set the app title
        self.root.geometry('1300x700')  # set the overall window size

        # Main frame setup
        main_frame = ttk.Frame(root, padding="10 10 10 10")  # add padding of the content rendered in the window
        main_frame.grid(column=0, row=0, sticky='nsew')  # use grid layout to arrange the items
        main_frame.columnconfigure(0, weight=1)  # Configure column 0 to expand with weight 1
        main_frame.rowconfigure(1, weight=1)  # Configure row 1 to expand with weight 1

        # Title label - ensure it is visible and correctly placed
        title_label = ttk.Label(main_frame, text="Traffic Volume", font=("Helvetica", 16))
        title_label.grid(column=0, row=0, sticky=tk.W, pady=10)

        # Configure canvas and scrollbars
        canvas = tk.Canvas(main_frame, width=1200)  # Create a Canvas widget inside the main_frame with a specified width
        canvas.grid(row=1, column=0, sticky='nsew')  # Place the canvas in the grid layout

        v_scroll = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)  # Create a vertical scrollbar
        h_scroll = ttk.Scrollbar(main_frame, orient='horizontal', command=canvas.xview)  # Create a horizontal scrollbar
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)  # Link scrollbars to canvas scrolling
        v_scroll.grid(row=1, column=1, sticky='ns')  # Place the vertical scrollbar in the grid layout
        h_scroll.grid(row=2, column=0, sticky='ew')   # Place the horizontal scrollbar in the grid layout

        # Frame for the Treeview
        tree_frame = ttk.Frame(canvas)  # Create a Treeview widget inside tree_frame
        tree_window = canvas.create_window((0, 0), window=tree_frame, anchor='nw')  # Pack the Treeview widget to fill the frame and expand with it

        # Treeview setup
        self.tree = ttk.Treeview(tree_frame, height=30, show='headings')
        self.tree.pack(fill='both', expand=True)
        columns = ('id', 'section_id', 'highway', 'section', 'section_length',
                   'section_description', 'date', 'description', 'group',
                   'type', 'county', 'ptrucks', 'adt', 'aadt', 'direction',
                   '85pct', 'priority_points')
        self.tree['columns'] = columns
        for col in columns:
            self.tree.heading(col, text=col.title().replace('_', ' '))
            self.tree.column(col, width=120)

        # Bind the canvas to resize based on the frame
        tree_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.tree.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox(tree_window)))

        # Buttons and footer
        ttk.Button(main_frame, text="Refresh", command=self.refresh_treeview).grid(row=3, column=0, sticky=tk.W,
                                                                                      pady=10)
        ttk.Button(main_frame, text="Check a Record", command=self.check_record).grid(row=4, column=0, sticky=tk.W, pady=10)
        ttk.Button(main_frame, text="Check Record(s) with details", command=self.check_record_with_details).grid(row=5,
                                                                                     column=0, sticky=tk.W, pady=10)
        ttk.Button(main_frame, text="Add a Record", command=self.add_record).grid(row=6, column=0, sticky=tk.W,
                                                                                      pady=10)
        ttk.Button(main_frame, text="Update a Record", command=self.update_record).grid(row=7, column=0, sticky=tk.W,
                                                                                  pady=10)
        ttk.Button(main_frame, text="Delete a Record", command=self.delete_record).grid(row=8, column=0, sticky=tk.W,
                                                                                  pady=10)
        ttk.Button(main_frame, text="Reload dataset", command=self.reload_data).grid(row=3, column=0, sticky=tk.E, pady=10)
        ttk.Button(main_frame, text="Close App", command=root.quit).grid(row=8, column=0, sticky=tk.E, pady=10)

        footer_label = ttk.Label(main_frame, text="© Copyright by Ka Yan Ieong 041070033 in 2024", font=("Helvetica", 10))
        footer_label.grid(row=20, column=0, sticky=tk.W, pady=20)

        # Load initial data
        self.refresh_treeview()

    def refresh_treeview(self):
        """ Clears the treeview and reloads data from the server. """
        self.clear_treeview()
        self.load_data()

    def clear_treeview(self):
        """ Clear all items in the treeview. """
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_data(self):
        """ Load data from the server and insert into the treeview. """
        url = 'http://127.0.0.1:8000/trafficdata/api/volumes/'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                for item in response.json():
                    nested_data = item['data']
                    values = tuple([item['id']] + [nested_data.get(col) for col in self.tree['columns'] if col != 'id'])
                    self.tree.insert('', 'end', values=values)
            else:
                messagebox.showerror("Error", "Failed to fetch data")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def check_record(self):
        """ Opens a new window to read a record by ID """
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Check Record")
        self.new_window.geometry("300x100")

        # Entry field for ID
        ttk.Label(self.new_window, text="Enter ID:").pack(side=tk.LEFT, padx=10, pady=10)
        self.id_entry = ttk.Entry(self.new_window, width=20)
        self.id_entry.pack(side=tk.LEFT, padx=10, pady=10)

        # Button to submit ID and fetch record
        ttk.Button(self.new_window, text="Fetch Record", command=self.fetch_record).pack(pady=10)

    def fetch_record(self):
        """ Fetches the record by ID from the API and displays the data """
        record_id = self.id_entry.get().strip()
        url = f'http://127.0.0.1:8000/trafficdata/api/volumes/{record_id}/'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                record_data = response.json()
                self.display_data_in_table(record_data)  # Call to display data in table
            else:
                messagebox.showerror("Error", f"Failed to fetch record: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_data_in_table(self, data):
        data_window = tk.Toplevel(self.root)
        data_window.title("Record Details")
        data_window.geometry("500x300")

        # Use Treeview to display data in table format
        tree = ttk.Treeview(data_window, columns=('Key', 'Value'), show='headings')
        tree.heading('Key', text='Key')
        tree.heading('Value', text='Value')
        tree.column('Key', width=100)
        tree.column('Value', width=400)
        tree.pack(fill='both', expand=True)

        nested_data = data.get('data', {})
        for key, value in nested_data.items():
            tree.insert('', 'end', values=(key, value))

    def add_record(self):
        """ Opens a new window to add a record """
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Add New Record")
        self.new_window.geometry("500x600")

        # Entry fields for each data attribute, keys should match the JSON structure exactly
        labels = ['section_id', 'highway', 'section', 'section_length', 'section_description', 'date', 'description',
                  'group', 'type', 'county', 'ptrucks', 'adt', 'aadt', 'direction', '85pct', 'priority_points']
        self.entries = {}
        for idx, label in enumerate(labels):
            formatted_label = " ".join(label.split('_')).title()  # Make labels user-friendly
            ttk.Label(self.new_window, text=formatted_label).grid(row=idx, column=0, sticky=tk.W)
            entry = ttk.Entry(self.new_window)
            entry.grid(row=idx, column=1, sticky=tk.W)
            self.entries[label] = entry  # Use API expected keys as entry dict keys

        # Submit button
        ttk.Button(self.new_window, text="Submit", command=self.submit_record).grid(row=len(labels), column=0,
                                                                                    columnspan=2)

    def submit_record(self):
        """ Collects the data from entry fields, creates a JSON payload, and sends it to the API """
        data = {key: entry.get() for key, entry in self.entries.items()}  # Gather data from entries
        payload = {'data': data}  # Wrap the data dictionary within another dictionary under 'data' key
        url = 'http://127.0.0.1:8000/trafficdata/api/volumes/create/'

        try:
            # Send POST request with JSON payload
            response = requests.post(url, json=payload)  # Use json parameter to convert dict to JSON automatically
            if response.status_code == 201:  # Check if creation was successful
                messagebox.showinfo("Success", "Record added successfully!")
            else:
                messagebox.showerror("Error", f"Failed to add record: {response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        self.new_window.destroy()  # Close the entry window

    def update_record(self):
        """ Opens a new window to update a record by ID """
        self.update_window = tk.Toplevel(self.root)
        self.update_window.title("Update Record")
        self.update_window.geometry("500x600")

        # Widgets for entering the ID to fetch
        ttk.Label(self.update_window, text="Enter ID:").grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = ttk.Entry(self.update_window, width=20)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.update_window, text="Fetch Record", command=self.fetch_record_for_update).grid(row=1, column=0,
                                                                                                       columnspan=2)

    def fetch_record_for_update(self):
        """ Fetches the record by ID and allows editing """
        record_id = self.id_entry.get().strip()
        url = f'http://127.0.0.1:8000/trafficdata/api/volumes/{record_id}/'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.record_data = response.json()
                self.show_record_data(self.record_data)
            else:
                messagebox.showerror("Error", f"Failed to fetch record: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_record_data(self, data):
        """ Displays the record data in editable fields """
        labels = ['section_id', 'highway', 'section', 'section_length', 'section_description', 'date', 'description',
                  'group', 'type', 'county', 'ptrucks', 'adt', 'aadt', 'direction', '85pct', 'priority_points']
        self.entries = {}
        row_start = 2  # Starting row index for the first entry

        for idx, label in enumerate(labels):
            # Format label for display
            formatted_label = label.replace('_', ' ').title()

            # Create label and entry widget for each field
            ttk.Label(self.update_window, text=formatted_label).grid(row=idx + row_start, column=0, padx=10, pady=2,
                                                                     sticky=tk.W)
            entry = ttk.Entry(self.update_window, width=20)
            entry.grid(row=idx + row_start, column=1, padx=10, pady=2, sticky=tk.W)

            # Check if the label is in data and preload it; handle nested 'data' dictionary if needed
            if 'data' in data and label in data['data']:
                entry.insert(0, data['data'][label])  # Preload the data into the entry field
            elif label in data:
                entry.insert(0, data[label])  # If data is not nested

            self.entries[label] = entry  # Store entry to collect data later

        # Button to submit the updated data
        ttk.Button(self.update_window, text="Submit Update", command=self.submit_update).grid(
            row=len(labels) + row_start, column=0, columnspan=2)

    def submit_update(self):
        """ Collects the updated data and sends it back to the server """
        updated_data = {key: entry.get() for key, entry in self.entries.items()}
        payload = {'data': updated_data}
        url = f'http://127.0.0.1:8000/trafficdata/api/volumes/update/{self.id_entry.get().strip()}/'

        try:
            response = requests.put(url, json=payload)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Record updated successfully!")
            else:
                messagebox.showerror("Error", f"Failed to update record: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        self.update_window.destroy()  # Close the update window

    def delete_record(self):
        """ Opens a new window to delete a record by ID """
        self.delete_window = tk.Toplevel(self.root)
        self.delete_window.title("Delete Record")
        self.delete_window.geometry("300x200")

        # Widgets for entering the ID to delete
        ttk.Label(self.delete_window, text="Enter ID to Delete:").pack(side=tk.TOP, padx=10, pady=10)
        self.delete_id_entry = ttk.Entry(self.delete_window, width=20)
        self.delete_id_entry.pack(side=tk.TOP, padx=10, pady=10)

        # Button to submit ID and delete record
        ttk.Button(self.delete_window, text="Delete Record", command=self.submit_delete).pack(side=tk.TOP, pady=20)

    def submit_delete(self):
        """ Sends a DELETE request to the server to remove the record """
        record_id = self.delete_id_entry.get().strip()
        if not record_id:
            messagebox.showwarning("Warning", "Please enter a valid ID.")
            return

        url = f'http://127.0.0.1:8000/trafficdata/api/volumes/delete/{record_id}/'

        try:
            response = requests.delete(url)
            if response.status_code == 204:  # HTTP 204 No Content, standard response for successful delete
                messagebox.showinfo("Success", "Record deleted successfully!")
            else:
                messagebox.showerror("Error", f"Failed to delete record: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        self.delete_window.destroy()  # Close the delete window

    def reload_data(self):
        """ Run the Django management command to reload data. """
        project_dir = Path('C:/Users/kyieo/PycharmProjects/CST8333/myproject')
        try:
            result = subprocess.run(
                ['python', 'manage.py', 'load_traffic_volumes'],
                cwd=project_dir,
                stdout=subprocess.PIPE,
                text=True
            )
            messagebox.showinfo("Reload Data", f"Reload Complete: {result.stdout}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload data: {str(e)}")

    def check_record_with_details(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Check Record(s) with Details")
        self.new_window.geometry("400x400")

        # Entry fields and labels
        ttk.Label(self.new_window, text="Enter Section ID:").pack(pady=10)
        self.section_id_entry = ttk.Entry(self.new_window, width=20)
        self.section_id_entry.pack(pady=10)

        ttk.Label(self.new_window, text="Enter Type:").pack(pady=10)
        self.type_entry = ttk.Entry(self.new_window, width=20)
        self.type_entry.pack(pady=10)

        ttk.Label(self.new_window, text="Enter Direction (Optional):").pack(pady=10)
        self.direction_entry = ttk.Entry(self.new_window, width=20)
        self.direction_entry.pack(pady=10)

        # Button to submit the data and fetch records
        ttk.Button(self.new_window, text="Fetch Record", command=self.fetch_record_with_details).pack(pady=20)

    def fetch_record_with_details(self):
        section_id = self.section_id_entry.get().strip()
        type = self.type_entry.get().strip()
        direction = self.direction_entry.get().strip() if self.direction_entry.get().strip() else None
        direction_param = f"?direction={direction}" if direction else ""
        url = f'http://127.0.0.1:8000/trafficdata/api/volumes/{section_id}/{type}/{direction_param}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                record_data = response.json()
                self.display_data_in_treeview(record_data)  # Call to display data in treeview
            else:
                messagebox.showerror("Error", f"Failed to fetch record: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_data_in_treeview(self, records):
        """ Displays fetched records in a detailed treeview format """
        data_window = tk.Toplevel(self.root)
        data_window.title("Record Details")
        data_window.geometry("600x700")

        tree = ttk.Treeview(data_window, columns=('ID', 'Key', 'Value'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Key', text='Key')
        tree.heading('Value', text='Value')
        tree.pack(expand=True, fill='both')

        # Populate the treeview with records
        for record in records:
            if 'id' in record and 'data' in record:
                record_id = record['id']
                # Insert each key-value pair directly under the ID
                for key, value in record['data'].items():
                    tree.insert('', 'end', values=(record_id, key, value))

        tree.column('ID', width=50)
        tree.column('Key', width=150)
        tree.column('Value', width=400)


if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = TrafficVolumeApp(root)  # Create an instance of the TrafficVolumeApp
    root.mainloop()  # Start the Tkinter event loop
