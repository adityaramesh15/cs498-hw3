import requests
import time
import json


BASE_URL = "http://136.115.119.151:5000"

payload = {
    "VIN (1-10)": "1N4AZ0CP",
    "County": "King",
    "City": "Seattle",
    "State": "WA",
    "Postal Code": "98101",
    "Model Year": "2023",
    "Make": "NISSAN",
    "Model": "LEAF",
    "Electric Vehicle Type": "Battery Electric Vehicle (BEV)"
}

headers = {'Content-Type': 'application/json'}

def measure_latency(endpoint, num_requests=50):
    url = f"{BASE_URL}{endpoint}"
    total_time = 0
    
    print(f"Starting {num_requests} requests to {endpoint}...")
    
    for i in range(num_requests):
        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers)
        
        end_time = time.time()
        
        if response.status_code == 201:
            duration_ms = (end_time - start_time) * 1000
            total_time += duration_ms
        else:
            print(f"Request {i+1} failed with status {response.status_code}")
            
    average_latency = total_time / num_requests
    print(f"Done! Average latency for {endpoint}: {average_latency:.2f} ms\n")

# Run the tests
if __name__ == "__main__":
    measure_latency("/insert-fast", 50)
    measure_latency("/insert-safe", 50)