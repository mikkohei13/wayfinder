
import requests
import json

from requests.auth import HTTPBasicAuth

# Load the configuration
with open('secrets.json', 'r') as file:
    config = json.load(file)


# This expects that the API always gives genus or species
def get_genus(taxon):
    if " " not in taxon:
        return taxon
    parts = taxon.split(" ")
    return parts[0]


def naturalis_id(image_path):

    username = config['naturalis_username']
    password = config['naturalis_password']
    token = config['naturalis_token']
    url = config['naturalis_url'] + token

    # Read the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Prepare the data for the POST request
        files = {
            "image": (image_path, image_file, "image/jpeg")
        }
        params = {
#            'force_submodel': 'Plantae',
#            "taxon_namespace": "FINBIF",
            "autozoom_enabled": 0
        }
        print(files, params)
        
        response = requests.post(
            url,
            files=files,
            data=params,
            auth=HTTPBasicAuth(username, password)
        )

        # Check if the request was successful
        if response.status_code == 200:
            # Convert the response JSON to a dictionary
            print(response.text) # DEBUG
            response_dict = json.loads(response.text)   
        else:
            print(f"Error: {response.status_code}")
            json_data = response.json()
            pretty_json = json.dumps(json_data, indent=4, sort_keys=True)
            print(pretty_json)
            exit()

    # Best match
    best_species = response_dict['predictions'][0]['taxa']['items'][0]['scientific_name']
    best_species_probability = round(response_dict['predictions'][0]['taxa']['items'][0]['probability'], 6)

    # Genera
    genera = dict()
    for prediction in response_dict['predictions'][0]['taxa']['items']:
        genus = get_genus(prediction['scientific_name'])
        if genus in genera:
            genera[genus] = genera[genus] + prediction['probability']
        else:
            genera[genus] = prediction['probability']
        
    # Best genus
    best_genus_dict = max(genera.items(), key=lambda x: x[1])
    best_genus, best_genus_probability = best_genus_dict
    best_genus_probability = round(best_genus_probability, 6)

    print("Successful identification")

    return best_species, best_species_probability, best_genus, best_genus_probability, response_dict
