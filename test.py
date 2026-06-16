# this is what querying the server looks like (dapat)
# but it only works locally

import requests

log_url = "http://localhost:8000/log"
url = "http://localhost:8000/verify"

payload = {
    "uid": "5408602380",
    "dob": "1997/09/12"
}

log_payload = {
    "message": "This is a log"
}

headers = {
    "x-api-key": "39983",
    "Content-Type": "application/json"
}

# response = requests.post(log_url, json=log_payload, headers=headers)
response = requests.post(url, json=payload, headers=headers)
print("Response:", response.json())
