import csv
import os

class DataHandler:
    def __init__(self, file_path):
        self.file_path = os.path.join(os.getcwd(), file_path)

    def save_data(self, data):
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def read_data(self):
        with open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            return list(reader)

    def save_final_data(self, data):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)