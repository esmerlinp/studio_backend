import requests
import sys

# Usage: python test_permissions.py <base_url> <token> <client_uuid>

if len(sys.argv) < 4:
    print("Usage: python test_permissions.py <base_url> <token> <client_uuid>")
    sys.exit(1)

base_url = sys.argv[1]
token = sys.argv[2]
client_uuid = sys.argv[3]

url = f"{base_url}/api/v1/user/permissions"
headers = {
    "Authorization": f"Bearer {token}"
}
params = {
    "client_uuid": client_uuid
}

try:
    response = requests.get(url, headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
