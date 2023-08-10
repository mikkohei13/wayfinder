
import os
import json

import naturalis_api


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
                full_path = os.path.join(dir_path, filename)

                best_species, best_species_probability, best_genus, best_genus_probability, taxon_id, response_dict = naturalis_api.naturalis_id(full_path, False) # False = mock data, True = real data 

                print("Here shall be data")
                print(best_species, best_species_probability, best_genus, best_genus_probability, taxon_id, response_dict)

                data_dict = dict()
                data_dict['best_species'] = best_species
                data_dict['best_species_probability'] = best_species_probability
                data_dict['best_genus'] = best_genus
                data_dict['best_genus_probability'] = best_genus_probability
                data_dict['response_dict'] = response_dict

                with open(full_data_path, 'w') as f:
                    json.dump(data_dict, f)

            # if identification data exists:
            else:
                print(f"Data exists for { filename }...")

