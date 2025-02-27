import http.client
import json
import csv

# API Connection Setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiOWU2MzdkODUtNGFmNS00ZDMxLTk1ODEtY2ExYWY4Nzc1YjRiLTE1NDU2NDk4MSIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiZF9ydUxpdk4tVVJOcFJjOGVQcWRad3JSclVrIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwNjM4MzQ1LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwNjM4MzQ1LCJyZWFsbSI6Ii8iLCJleHAiOjE3NDA2MzkyNDUsImlhdCI6MTc0MDYzODM0NSwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJpUVhiM2kyME5fRWszWUgtNGRJLWhlSjFWQnciLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.f_cZKiCQDwEnVQLvo3840GWJmGs4m5gE1d8tna0IrdAlWFXyoczyRdpPsrqaU80gqRa8YWdaEPJMrRcI6Xwx9itWqmp5o1JuG7ulIBoWSXW1hq-uq40EWkvOQzrCXnjVNAxYl4diKySogTqcy5JcNmDQrciZcJQPex-3MQYDoivgGizkWe2amDvgAmjC-HKIsnLFGZlXgs8mgAFYnslF0EZrXiJLzV8w83pSHjmdSVPfb75DANP2V0V3ThzS53pe4HJ_evGP6-NLokHAvIL_MFXBV8n6pyh2Ua3Fel0MmFnUH3akGDS486-6ICKmVXWMoFfWA3PZmcUvVEXMaap-mw'
}

# Position Menu
position_options = {
    "1": "pre",
    "2": "post"
}

folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# User selects Position
print("\nSelect Position:")
for key, value in position_options.items():
    print(f"{key}. {value.capitalize()}")

position_choice = input("Enter the number for Position: ").strip()
position = position_options.get(position_choice, "pre")  # Default to "pre" if invalid

# User selects Folder
print("\nSelect Folder:")
for key, value in folder_options.items():
    print(f"{key}. {value}")

folder_choice = input("Enter the number for Folder: ").strip()
folder = folder_options.get(folder_choice, "Shared")  # Default to "Shared" if invalid

print(f"\nUsing Position: {position}, Folder: {folder}\n")

# File Path
policy_file = r"C:\Users\DELL\Desktop\output\export_policies_security_rulebase3.csv"

# Read CSV and Upload Policies
with open(policy_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)

    seen_names = set()  # Track already processed policy names

    for row in reader:
        policy_name = row.get("Name", "").strip()
        if not policy_name:
            print("Skipping row with missing policy name.")
            continue

        if policy_name in seen_names:
            continue  
        seen_names.add(policy_name)

        # Extract and process Source Address
        raw_source_address = row.get("Source Address", "any").strip()
        source_address_list = [addr.strip() for addr in raw_source_address.split(";") if addr.strip()]

        # Debugging output
        print(f"\nProcessing Policy: {policy_name}")
        print(f"Source Address (Raw): '{raw_source_address}'")
        print(f"Source Address (Processed): {source_address_list}")

        # Updated payload: Replaced "source_address" with "source"
        payload = {
            "name": policy_name,
            "action": row.get("Action", "deny").strip(),
            "application": [app.strip() for app in row.get("Application", "any").split(";") if app.strip()],
            "category": [cat.strip() for cat in row.get("Category", "any").split(";") if cat.strip()],
            "destination": [dest.strip() for dest in row.get("Destination Address", "any").split(";") if dest.strip()],
            "service": [svc.strip() for svc in row.get("Service", "any").split(";") if svc.strip()],
            "from": [src_zone.strip() for src_zone in row.get("Source Zone", "any").split(";") if src_zone.strip()],
            "to": [dest_zone.strip() for dest_zone in row.get("Destination Zone", "any").split(";") if dest_zone.strip()],
            "source": source_address_list if source_address_list else ["any"],  # Updated field
            "source_user": [usr.strip() for usr in row.get("Source User", "any").split(";") if usr.strip()]
        }

        # Print the final payload before sending
        print("Final Payload JSON:", json.dumps(payload, indent=4))

        # API Request with Selected Position and Folder
        api_url = f"/sse/config/v1/security-rules?position={position}&folder={folder.replace(' ', '%20')}"
        conn.request("POST", api_url, json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read()

        response = data.decode("utf-8")
        print(f"Response for {policy_name}: {response}")  
