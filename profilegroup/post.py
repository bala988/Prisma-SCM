import http.client
import json
import csv

# API Connection Setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiNGZiYTJiMzItY2E0OC00YTE5LWIwMmMtYjYxNjFmNzQ1NDUwLTEzMDEzNTQ1NyIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiUnBNazhLSHJUczhVb29TdTZFcFM1bnBCYlpNIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwMTQxODgxLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwMTQxODgxLCJyZWFsbSI6Ii8iLCJleHAiOjE3NDAxNDI3ODEsImlhdCI6MTc0MDE0MTg4MSwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJmTTQtNkNQckxfMmpHTlJUNm9YRHpJOHlzTDgiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.k7rW9U4Mp588xtL4ph0jaL-5g-8R5Qr6F9P-DYZid2wG04ObMKRTFmayjqR1D-mzNYTtQvH_HkjgulmN7WaTJ4WsXNYEsFHa7XjcyttoeLTKXGt4Mtie-VbP-pM1bt-hgCdFh6JcOVKsFyVJV2qdTWfD0nvg1EdTxUsD2okWM9d9CmllTFSJfOmkW-pLuBX8-wtwQF_TG1nHr8whb4QmqbGHWjNkstkGIgrea6D3ezXGANIAsNKKlwxHGClHV7SbDrX0vLSP4kPG0ODPdhKlbF2O-KHZSwljeOS5yFBcIjlV03vzIkb898oVnk2N3zo9HC_01LvYOCagCs69e0aYQg'
}

# Folder Menu
folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Mobile Users Container",
    "5": "Mobile Users Explicit Proxy"
}

# User selects Folder
print("\nSelect Folder:")
for key, value in folder_options.items():
    print(f"{key}. {value}")

folder_choice = input("Enter the number for Folder: ").strip()
folder = folder_options.get(folder_choice, "Shared")

print(f"\nUsing Folder: {folder}\n")

# CSV File Path
csv_file_path = r"C:\Users\DELL\Desktop\output\export_objects_security_profile-groups.csv"

# Read CSV and send API requests
with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row.get("Name", "").strip()
        #spyware = row.get("Anti Spyware Profile", "").strip()  # Ensure column name is correct
        
        if not name:
            print(f"Skipping row due to missing name: {row}")
            continue
        
        payload = json.dumps({
            #"dns_security": row.get("dns_security", "").split(','),
            "file_blocking": row.get("File Blocking Profile", "").split(','),
            "name": name,
            #"saas_security": row.get("saas_security", "").split(','),
            "Spyware": row.get("Anti Spyware Profile", "").split(','),
            #"url_filtering": row.get("url_filtering", "").split(','),
            #"virus_and_wildfire_analysis": row.get("virus_and_wildfire_analysis", "").split(','),
            "vulnerability": row.get("Vulnerability Protection Profile", "").split(',')
        })
        
        # Send API request with correct endpoint
        api_url = f"/sse/config/v1/profile-groups?folder={folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close the connection
conn.close()
