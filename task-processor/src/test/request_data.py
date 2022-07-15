TEST_URL = "http://localhost:5000/test"
FUNCTIONAL_URL = "http://localhost:5000/functionality"
EMAIL_URL = "http://localhost:5000/functionality?request_type=email"
EMAIL_STATUS_URL = "http://localhost:5000/email_status"

xml_data = ""
json_data = {
    "data": [
       {
            "Material Description": "MICRO",
            "Product Hierarchy": "US",
            "Material Type": "Abrasives ht",
            "Material Group": "4830",
            "Status":"hello",
            "Logical System Group": "us igs_' [] () _"
        },
        {
            "Material Description": "MICRO",
            "Product Hierarchy": "US",
            "Material Type": "Abrasives ht",
            "Material Group": "4830",
            "Status":"hello",
            "Logical System Group": "us igs_' [] () _"
        }
    ],
    "code": "QORVO_HTS"
}
expected_resp_json_xml = {
    "data": {
        "message": "14c32286-6081-40f2-9bc6-040b538d6a66",
        "responseCode": 200,
        "result": []
    }
}
email_data = {
    "first_name": "Ankit",
    "last_name": "",
    "to": "ankit.suwal@avyay.solutions",
    "subject": "Unit Test email.",
    "body": "This email test for unit test.",
    "send_time": ""
}

email_expected_data = {
    "data": {
        "message": "Email sent successfully.",
        "responseCode": 200,
        "result": []
    }
}

check_email = { "email": "ankit.suwal@avyay.solutions" }
