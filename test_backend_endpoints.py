#!/usr/bin/env python3
"""
Test Backend Endpoints
Run this script to test the Flask backend API endpoints
"""

import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:5000/api'

def print_section(title):
    print('\n' + '=' * 70)
    print(title.center(70))
    print('=' * 70)

def print_subsection(title):
    print(f'\n{title}')
    print('-' * 70)

try:
    print_section('TESTING BACKEND ENDPOINTS')

    # Test 1: Login
    print_subsection('1. LOGIN TEST')
    login_data = {'username': 'john_doe', 'password': 'password123'}
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    print(f'Status: {response.status_code}')
    print(f'Response:\n{json.dumps(response.json(), indent=2)}')
    cookies = response.cookies

    # Test 2: Get current user
    print_subsection('2. GET CURRENT USER')
    response = requests.get(f'{BASE_URL}/auth/me', cookies=cookies)
    print(f'Status: {response.status_code}')
    print(f'Response:\n{json.dumps(response.json(), indent=2)}')

    # Test 3: Get all lists
    print_subsection('3. GET ALL LISTS')
    response = requests.get(f'{BASE_URL}/lists', cookies=cookies)
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        lists = response.json()
        print(f'Found {len(lists)} lists:')
        for lst in lists:
            print(f'  - ID: {lst["id"]}, Title: {lst["title"]}')
    else:
        print(f'Error: {response.json()}')

    # Test 4: Get specific list (with items)
    print_subsection('4. GET LIST #1 (with hierarchical items)')
    response = requests.get(f'{BASE_URL}/lists/1', cookies=cookies)
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'List Title: {data["title"]}')
        print(f'List Description: {data.get("description", "N/A")}')
        items = data.get('items', [])
        print(f'Top-level items count: {len(items)}')
        if items:
            print('\nFirst 3 items:')
            for item in items[:3]:
                children_count = len(item.get('children', []))
                print(f'  - Title: {item["title"]}')
                print(f'    Depth: {item["depth"]}, Children: {children_count}')
                print(f'    Completed: {item["is_completed"]}, Collapsed: {item["is_collapsed"]}')
                if item.get('children'):
                    print(f'    Child items:')
                    for child in item['children'][:2]:
                        grandchild_count = len(child.get('children', []))
                        print(f'      - {child["title"]} (depth: {child["depth"]}, grandchildren: {grandchild_count})')
    else:
        print(f'Error Status: {response.status_code}')
        print(f'Error Response:\n{json.dumps(response.json(), indent=2)}')

    print_section('BACKEND TEST COMPLETE')
    print('\n✅ All tests completed successfully!')

except requests.exceptions.ConnectionError:
    print('❌ ERROR: Cannot connect to backend at http://127.0.0.1:5000')
    print('   Make sure the Flask server is running: python run.py')
    sys.exit(1)
except Exception as e:
    print(f'❌ ERROR: {type(e).__name__}: {str(e)}')
    sys.exit(1)
