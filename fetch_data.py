import requests
import json

SERVER_URL = "192.168.18.12" # Change after actual Hosting
URL = "http://"+ SERVER_URL +"/api/" # Base url
"""
Hard Code the API_KEY of bot. After allocating in the database.
"""
API_KEY =  "v18JqRute0GKwNi4As9wDFJKW" # Thrissur
## OR
# API_KEY =  "BYiqDUncnNkgmm6Zlw6KX7HUj" # Ernakulam


def get_active_bed_data():
    #Active beds
    ACTIVE_BEDS_URL = URL + "active_beds/"
    JSON_DATA = {"API_KEY": API_KEY}

    response = requests.post(ACTIVE_BEDS_URL, json=JSON_DATA)
    # print(json.loads(response.text)) # Comment after use
    active_beds = json.loads(response.text) # Convert JSON to Python Dict
    return active_beds

def get_patient_details(BED_ID):
    # Patient Details
    PATIENT_DETAILS_URL = URL + "patient_details/"
    JSON_DATA = {"API_KEY": API_KEY, "bed_name": BED_ID}
    response = requests.post(PATIENT_DETAILS_URL, json=JSON_DATA)
    # print(json.loads(response.text)) # Comment After use
    patient_details = json.loads(response.text) # Convert JSON to Python Dict
    return patient_details
