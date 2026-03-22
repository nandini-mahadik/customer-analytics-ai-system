"""
import requests

url = "http://127.0.0.1:5000/predict_purchase"

data = {
    "Frequency": 2,
    "Monetary": 5000,
    "Avg_Order_Value": 2500
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
"""

import requests

url = "http://127.0.0.1:5000/predict_churn"

data = {
    "Frequency": 1,
    "Monetary": 1000,
    "Avg_Order_Value": 1000
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())