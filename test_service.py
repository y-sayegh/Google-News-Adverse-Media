#!/usr/bin/env python3
"""
Test script for the Google News Adverse Media Search Service

This script demonstrates how to use the web service to search for adverse media.
Make sure the service is running (python app.py) before running this test.
"""

import requests
import json
import time

# Service configuration
SERVICE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/health", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_adverse_media_search():
    """Test the adverse media search endpoint"""
    print("\nTesting adverse media search endpoint...")
    
    # Test data
    test_payload = {
        "api_key": "test_api_key_123",
        "search_subject": "Tesla",
        "adverse_keywords": ["lawsuit", "investigation", "fraud", "scandal", "recall"]
    }
    
    try:
        print(f"Sending request with payload: {json.dumps(test_payload, indent=2)}")
        
        response = requests.post(
            f"{SERVICE_URL}/search",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Print summary
            if result['status'] == 'success':
                data = result['data']
                print(f"\n--- SEARCH RESULTS SUMMARY ---")
                print(f"Total articles found: {data['total_count']}")
                
                if data['results']:
                    print(f"\nTop results:")
                    for i, article in enumerate(data['results'][:3], 1):
                        print(f"{i}. {article['title']}")
                        print(f"   Relevance: {article['relevance_score']}")
                        print(f"   Summary: {article['summary'][:100]}...")
                        print(f"   Link: {article['link']}")
                        print()
                else:
                    print("No relevant articles found.")
            
        else:
            print(f"Error Response: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"Search test failed: {e}")
        return False

def test_invalid_request():
    """Test the service with invalid requests"""
    print("\nTesting invalid request handling...")
    
    # Test with missing fields
    invalid_payload = {
        "api_key": "test_key",
        "search_subject": "Tesla"
        # Missing adverse_keywords
    }
    
    try:
        response = requests.post(
            f"{SERVICE_URL}/search",
            json=invalid_payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code == 400
        
    except Exception as e:
        print(f"Invalid request test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Google News Adverse Media Search Service Test ===\n")
    
    # Check if service is running
    if not test_health_check():
        print("\n❌ Service health check failed. Make sure the service is running with 'python app.py'")
        return
    
    print("✅ Service is healthy")
    
    # Wait a moment before running tests
    time.sleep(1)
    
    # Run tests
    tests = [
        ("Adverse Media Search", test_adverse_media_search),
        ("Invalid Request Handling", test_invalid_request)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            print(f"✅ {test_name} passed")
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n=== TEST RESULTS ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the service logs for details.")

if __name__ == "__main__":
    main()
