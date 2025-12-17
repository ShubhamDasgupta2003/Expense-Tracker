# test_upload.py (Corrected script for file upload)
import requests
import json

url = 'http://127.0.0.1:5000/api/upload'
file_path = "./DecemberExpenses.csv"

try:
    # Open the file in binary read mode ('rb')
    with open(file_path, 'rb') as f:
        # Use the 'files' parameter, NOT 'json'
        # The key 'file' must match what your Flask code expects (request.files['file'])
        files = {'file': (file_path, f, 'text/csv')}
        
        response = requests.post(url, files=files)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Print the response cleanly
        print("\n--- Response from Flask Server ---")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        print("----------------------------------\n")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
