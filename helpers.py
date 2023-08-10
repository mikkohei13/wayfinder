
import os
import json
import requests

import naturalis_api

# Load the configuration
with open('secrets.json', 'r') as file:
    config = json.load(file)


def get_photo_list(dir_path):
    files = []
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(".jpg"):
            full_path = os.path.join(dir_path, filename)
            if os.path.isfile(full_path):
                files.append(filename)
    return files


def create_html(data_dict):
    # Note: html will be wrapped in a <p>
#    print(data_dict)

    if data_dict["best_species_probability"] >= 0.993:
        css_class = "highprob"
    elif data_dict["best_species_probability"] <= 0.8:
        css_class = "lowprob"
    else:
        css_class = "medprob"

    if data_dict['taxon_id']:

        url = f"https://api.laji.fi/v0/taxa/{ data_dict['taxon_id'] }?lang=fi&langFallback=true&maxLevel=0&includeHidden=false&includeMedia=false&includeDescriptions=false&includeRedListEvaluations=false&sortOrder=taxonomic&access_token="
        taxon_data = fetch_finbif_api(url)
        print(taxon_data)

        vernacular_name = taxon_data.get('vernacularName', 'ei suomenkielistä nimeä')
        fin_obs_count = taxon_data.get('occurrenceCountFinland', 0)

        if "typeOfOccurrenceInFinland" in taxon_data:
            fin_occurrence_type = ", ".join(taxon_data["typeOfOccurrenceInFinland"])
        else:
            fin_occurrence_type = "ei esiintymistietoa"
        
        species_page_url = f"https://laji.fi/taxon/{ data_dict['taxon_id'] }"

        parent_order = taxon_data["parent"]["order"]["scientificName"]
        parent_class = taxon_data["parent"]["class"]["scientificName"]

        html = (
            f"{ parent_class }: { parent_order }:<br>\n"
            f"<strong class='{ css_class }'>{ vernacular_name } <em>{ data_dict['best_species'] }</em> - { data_dict['best_species_probability'] }</strong><br>\n"
            f"{ fin_obs_count } havaintoa Suomesta, { fin_occurrence_type } (<a href='{ species_page_url }' target='_blank'>lajisivu</a>)<br>\n"
            f"&nbsp;<br>\n"
            f"<em>{ data_dict['best_genus'] }</em> - { data_dict['best_genus_probability'] }\n"
        )

    else:
        html = (
            f"<strong class='{ css_class }'><em>{ data_dict['best_species'] }</em> - { data_dict['best_species_probability'] }</strong><br>\n"
            f"EI TAKSONIN ID:ta"
            f"&nbsp;<br>\n"
            f"<em>{ data_dict['best_genus'] }</em> - { data_dict['best_genus_probability'] }\n"
        )

    return html


# Gets identification from Naturalis and saves the resulting data to disk as JSON. if the file exists already, does nothing.
def get_identifications(dir_path):
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(".jpg"):
            print(filename)
            data_filename = filename + ".json"
            full_data_path = os.path.join(dir_path, data_filename)

            # if identification data is missing:
            if not os.path.exists(full_data_path):
                full_path = os.path.join(dir_path, filename)

                best_species, best_species_probability, best_genus, best_genus_probability, taxon_id, response_dict = naturalis_api.naturalis_id(full_path, True) # False = mock data, True = real data 

                print("Debug:")
                print(best_species, best_species_probability, best_genus, best_genus_probability, taxon_id, response_dict)

                data_dict = dict()
                data_dict['best_species'] = best_species
                data_dict['best_species_probability'] = best_species_probability
                data_dict['best_genus'] = best_genus
                data_dict['best_genus_probability'] = best_genus_probability
                data_dict['taxon_id'] = taxon_id
                data_dict['response_dict'] = response_dict

                data_dict['html'] = create_html(data_dict)

                with open(full_data_path, 'w') as f:
                    json.dump(data_dict, f)

                print(f"Saved data for { filename }")

            # if identification data exists:
            else:
                print(f"Data exists for { filename }")


def fetch_finbif_api(api_url, log = False):
    if "&access_token=" not in api_url:
        print("DEV WARNING: access_token param is missing from your url!")

    api_url = api_url + config["finbif_token"]
    print("Fetching API: " + api_url)

    if log:
        print(api_url)

    try:
        r = requests.get(api_url)
    except ConnectionError:
        print("ERROR: api.laji.fi complete error.")

#    r.encoding = encoding
    dataJson = r.text
    dataDict = json.loads(dataJson)

    if "status" in dataDict:
        if 403 == dataDict["status"]:
            print("ERROR: api.laji.fi 403 error.")
            raise ConnectionError

#    print(dataDict)
    return dataDict


def fetch_api(api_url, log = False):
    if log:
        print(api_url)

    try:
        r = requests.get(api_url)
    except ConnectionError:
        print("ERROR: api.laji.fi complete error.")

#    r.encoding = encoding
    dataJson = r.text
    dataDict = json.loads(dataJson)

    if "status" in dataDict:
        if 403 == dataDict["status"]:
            print("ERROR: api.laji.fi 403 error.")
            raise ConnectionError

#    print(dataDict)
    return dataDict
