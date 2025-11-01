#!/usr/bin/env python3
"""
Test Backend - Debug GET LIST endpoint
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api'

# Login
login_data = {'username': 'john_doe', 'password': 'password123'}
response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
cookies = response.cookies

# Try to get list
print("Getting List #1...")
response = requests.get(f'{BASE_URL}/lists/1', cookies=cookies)
print(f"Status Code: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"\nResponse Text (first 2000 chars):")
print(response.text[:2000])

if response.status_code != 200:
    print(f"\n❌ ERROR! Full response text:")
    print(response.text)
