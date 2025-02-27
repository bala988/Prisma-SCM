import http.client
import json
import csv

# Mapping folder numbers to API folder names
FOLDER_MAP = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# API Token (Replace with your actual token)
AUTH_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiOWQ5MjYyZDgtMTE4YS00ZDYwLWExYzItZDY4ZTJlOTYzMWQ5LTE0NTY4NzI1OCIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiSzE5YVhRaGVucHBsUHk4bVltem5EWW9EMmlrIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwNDc5Nzk0LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwNDc5Nzk0LCJyZWFsbSI6Ii8iLCJleHAiOjE3NDA0ODA2OTQsImlhdCI6MTc0MDQ3OTc5NCwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJoRU1CdlhoSkY5YTdET1drOVhHRkkyN3BFV3MiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.SMYP7KdaPTUGXUrmwOJ-3lbPJhhKfzUIKMxkbEoCHK-3PQBwhRqjVi_TWZaP18iRovjZ174Bg6kUpRHDq0jzHwYHqyXJ7Al69pc6M_JRbaDTbId6fLE82ztVcXKxfefVokn4WRh9d64WmOhi8r3muslucGNagQPtRJbusUoA3IhEqqSJPEHItuc1PU0ck6_-7FmmvQYbPSi4FqADKUbGtQX0qR1KdcMGUQXadUh9JuriEjfI5qOrYW-gOKH14phxu13BpLR07E5M3ckf1Vg1bCThopsHGVhJb9XuUJrzn0AMrtzP8fhV3jGpvEfxtbihLQxAPgD636QYKPLR6nap5g"

# Function to process CSV and send API requests
def process_csv(csv_file, folder):
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.get("Name", "").strip()
            members = row.get("Members", "").strip().split(";")  # Split members by semicolon
            tags = row.get("Tags", "").strip().split(";") if row.get("Tags") else []

            # Validate necessary fields
            if not name or not members or all(m.strip() == "" for m in members):
                print(f"Skipping row due to missing name or service group members: {row}")
                continue

            # Prepare payload
            payload = {
                "name": name,
                "members": members,
                #"tag": tags
            }

            send_request(payload, folder)

# Function to send API request
def send_request(payload, folder):
    conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': AUTH_TOKEN
    }

    endpoint = f"/sse/config/v1/service-groups?folder={folder.replace(' ', '%20')}"
    conn.request("POST", endpoint, json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()
    print(f"Response for {payload['name']}: {data.decode('utf-8')}")

# Get user input for folder selection
print("Select the target folder:")
for key, value in FOLDER_MAP.items():
    print(f"{key}. {value}")

folder_choice = input("Enter the number corresponding to the folder: ").strip()
selected_folder = FOLDER_MAP.get(folder_choice)

if not selected_folder:
    print("Invalid selection. Exiting.")
else:
    csv_file = "C:\\Users\\DELL\\Desktop\\output\\export_objects_service_groups1.csv"  # Update path as needed
    process_csv(csv_file, selected_folder)
