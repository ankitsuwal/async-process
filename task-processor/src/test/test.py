import json
import unittest
import requests
from request_data import EMAIL_URL, xml_data, json_data, check_email, email_data, TEST_URL, EMAIL_STATUS_URL,FUNCTIONAL_URL, EMAIL_URL, expected_resp_json_xml, email_expected_data
# from api import test, functionality
class TestApi(unittest.TestCase):
    
    def test_1_test(self):
        resp = requests.get(TEST_URL)
        self.assertEqual(resp.status_code, 200)
        print("Test 1 is completed.")
    
    def test_2_functionality_json(self):
        resp = requests.post(FUNCTIONAL_URL, json=json_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["data"]["responseCode"], 
                         expected_resp_json_xml["data"]["responseCode"])
        print("Test 2 with json data is completed.")
        
    def test_3_functionality_xml(self):
        resp = requests.post(FUNCTIONAL_URL, json=xml_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["data"]["responseCode"], 
                         expected_resp_json_xml["data"]["responseCode"])
        print("Test 3 with xml data is completed.")
        
    def test_4_email(self):
        resp = requests.post(EMAIL_URL, json=email_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['responseCode'], 
                         email_expected_data['data']['responseCode'])
        print("Test 4 with email data is completed.")

    def test_5_email_status(self):
        resp = requests.get(EMAIL_STATUS_URL, json=check_email)
        self.assertEqual(resp.status_code, 200)
        print("Test 5 check email status is completed.")
        
if __name__ == "__main__": 
    tester = TestApi()
    tester.test_1_test()
    tester.test_2_functionality_json()
    # tester.test_3_functionality_xml()
    tester.test_4_email()
    tester.test_5_email_status()