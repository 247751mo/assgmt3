import requests

BASE_URL = 'http://127.0.0.1:5000/api/data'

def test_get_data():
    response = requests.get(BASE_URL)
    print("GET /api/data:")
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())  # Properly print JSON response
    except requests.exceptions.JSONDecodeError as e:
        print("Error decoding JSON. Response text:", response.text)  # Print raw response text
    print("-" * 50)

def test_post_data():
    data = {
        'hours_studied': 3.5,
        'sleep_hours': 7,
        'performance_level': 2
    }

    response = requests.post(BASE_URL, json=data)
    print("POST /api/data:")
    print("Status Code:", response.status_code)

    try:
        print("Response JSON:", response.json())  # Correctly handling JSON response
    except requests.exceptions.JSONDecodeError as e:
        print("Error decoding JSON. Response text:", response.text)
    print("-" * 50)

def test_delete_data(record_id):
    response = requests.delete(f"{BASE_URL}/{record_id}")
    print(f"DELETE /api/data/{record_id}:")
    print("Status Code:", response.status_code)

    try:
        print("Response JSON:", response.json())  # Properly handle and print the response
    except requests.exceptions.JSONDecodeError as e:
        print("Error decoding JSON. Response text:", response.text)
    print("-" * 50)

def main():
    test_get_data()  # Test GET request
    test_post_data()  # Test POST request
    test_delete_data(2)  # Test DELETE request (adjust ID as needed)

if __name__ == "__main__":
    main()
