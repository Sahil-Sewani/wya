import requests
import json

# Define the URL of your Flask API
api_url = 'http://127.0.0.1:5000/add_package'  # Replace with your API URL

# Sample data for adding a package
data = {
    "package_name": "Sample Package",
    "tracking_number": "ABC123",
    "user_id": 7  # Replace with the actual user_id or authentication token
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Send POST request to the API endpoint
response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json_data)

# Print the response
print("Response status code:", response.status_code)
print("Response data:", response.text)  # Print the response text directly







