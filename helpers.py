
import os

def get_photo_list(dir_path):
    files = []
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(".jpg"):
            full_path = os.path.join(dir_path, filename)
            if os.path.isfile(full_path):
                files.append(filename)

    return files

def get_identifications(dir_path):
    files = []
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(".jpg"):
            print(filename)
            data_filename = filename + ".json"
            full_data_path = os.path.join(dir_path, data_filename)
            # if identification data is missing:
            if not os.path.exists(full_data_path):
                print(f"GETTING DATA FOR { filename }...")
            else:
                print(f"Data exists for { filename }...")

