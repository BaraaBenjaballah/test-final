import requests
import json

# Configuration
api_url = "https://your-acunetix-instance/api/v1/"
api_key = "your-api-key"

# Démarrer un scan
def start_scan(target_url):
    endpoint = "scans"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "target": target_url
    }
    response = requests.post(f"{api_url}{endpoint}", headers=headers, json=payload)
    if response.status_code == 201:
        scan_id = response.json()["id"]
        print(f"Scan started with ID: {scan_id}")
        return scan_id
    else:
        print(f"Failed to start scan: {response.text}")
        return None

# Obtenir les résultats du scan
def get_scan_results(scan_id):
    endpoint = f"scans/{scan_id}/results"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(f"{api_url}{endpoint}", headers=headers)
    if response.status_code == 200:
        results = response.json()
        print(json.dumps(results, indent=2))
    else:
        print(f"Failed to get scan results: {response.text}")

# Exemple d'utilisation
target_url = "http://example.com"
scan_id = start_scan(target_url)
if scan_id:
    get_scan_results(scan_id)
