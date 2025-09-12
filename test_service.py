#!/usr/bin/env python3
"""
Test script for the Email Forwarding Service
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8080"
TOKEN = "demo_token_abc123"  # Update with your token

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health Status: {response.status_code}")
        print(f"📊 Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_send_email():
    """Test sending an email"""
    print("\n📧 Testing email sending...")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": "Test Email from API",
        "message": "This is a test message.\nIt supports multiple lines.\n\nKind regards,\nEmail Service Test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/send", headers=headers, json=data)
        print(f"✅ Send Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"📬 Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Send test failed: {e}")
        return False

def test_invalid_token():
    """Test with invalid token"""
    print("\n🔒 Testing invalid token...")
    
    headers = {
        "Authorization": "Bearer invalid-token",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": "Test Email",
        "message": "This should fail"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/send", headers=headers, json=data)
        print(f"🔑 Auth Test Status: {response.status_code}")
        
        if response.status_code == 403:
            print("✅ Authentication properly rejected invalid token")
            return True
        else:
            print(f"❌ Unexpected response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Auth test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Email Forwarding Service Test Suite")
    print("=" * 50)
    
    tests = [
        test_health,
        test_send_email,
        test_invalid_token
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()