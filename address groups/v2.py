import csv
import http.client
import json

# Define API connection
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiYmY5MzYwYjQtY2Q5YS00MzM2LWJmODYtZTllNDkwMGVjZmQzLTE1MDgwODQ5NyIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiejNwMzYya29nc184VlhmZEpNWlpyMG5OckhjIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwNTc1OTE4LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwNTc1OTE4LCJyZWFsbSI6Ii8iLCJleHAiOjE3NDA1NzY4MTgsImlhdCI6MTc0MDU3NTkxOCwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJzUHRXNGxuck1KdGt6R3doUWRFQV9va3Y0VFkiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.hr80Qv56rZQrV9rlCugLlEP6_1asHktfI7PgOSoqe8CnNFzwuzPwqUUgdCwLnKQjur2W21Gj4MJYKrBX7TtJ1Gl0TXl0EH3NxjMf325EOwdDB_lYphOsqENtiLrPMCdfq_DVyU-Ilg6l54_3yHKZKB8qns1iozFxnZW54QzXufjlebgUSWbihBmMfaZhbYxD7rUus5g6GySVtTOBwByPItpqqHXoYGYEvC6Hj27uSeTOVwx3umzUe-xzP_GT2913pPOqKujfxs91vsbY9XJf6hSkmQLSRubnJ5Y6U1w7XssRsL9ODm8zzNfm5nr9Fp8Kxqzn-4rl0aA34UuugmEguQ'
}

# Folder options for Address Groups
folders = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# Display folder options
print("Select a folder to add address groups:")
for key, value in folders.items():
    print(f"{key}. {value}")

# Get user input for folder selection
selected_option = input("Enter the number corresponding to the folder: ").strip()

# Validate user input
if selected_option not in folders:
    print("Invalid selection. Exiting...")
    exit()

selected_folder = folders[selected_option]

# CSV File Path
csv_file = r"C:\Users\DELL\Desktop\output\export_objects_address_groups.csv"

# Read CSV and push address groups to Prisma Access
with open(csv_file, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Extract values
        name = row.get("Name", "").strip()
        description = row.get("Description", "").strip()
        addresses = row.get("Addresses", "").strip()  # Now using "Addresses" instead of "Static"
        tag = row.get("Tags", "").strip()

        # Skip rows with missing essential fields
        if not name or not addresses:
            print(f"Skipping row due to missing name or address group members: {row}")
            continue

        # Convert address objects from semicolon-separated format to list
        address_list = [addr.strip() for addr in addresses.split(";")]

        payload = json.dumps({
            "description": description if description else f"Auto-imported address group {name}",
            "name": name,
            "tag": [tag] if tag else [],
            "static": address_list
        })

        # Send API request to the selected folder
        api_url = f"/sse/config/v1/address-groups?folder={selected_folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close the connection
conn.close()
