import fetch_data
""" 
Testing Functions
"""

active_beds_temp = fetch_data.get_active_bed_data()
print(active_beds_temp)
active_beds = active_beds_temp.get('beds')
print(active_beds)
"""
Sample Output:
{'beds': ['A1', 'C13']}
""" 




"""
Bed Id. Temorarily setting as first bed id from the active bed list. 
Change as required later (Programatically)
BED_ID = ACTIVE_BED["beds"][0] 
"""
#BED_ID = active_beds["beds"][0]

#patient_details = fetch_data.get_patient_details(BED_ID)
#print(patient_details)
"""
Sample Output:
{'data': {'section': 1, 'bed_name': 'A1', 'category': 'Category A', 'name': 'ABC', 'age': 50, 'phone': '1234567890', 'swab_collection_date': '2020-07-28', 'status': 'Admitted', 'created': '2020-08-04T06:03:23.829Z', 'last_updated': '2020-08-04T06:03:23.829Z'}}
"""
