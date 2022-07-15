import os
import json
import pytz

import time
from datetime import datetime
import smtplib, ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from libraries.custom_errors import CustomErrors
import re
 
# regular expression for validating an Email
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class Email:
    """
    Class will login to gmail account
    send_email: send an email.
    send_email_at: send an email at specific time.
    """
    def __init__(self, data):
    
    # def __init__(self, subject, first_name, body, to, send_time):
        # connection configurartion
        self.port = 465  # For SSL
        self.smtp_server = "smtp.gmail.com"
        
        # email components
        self.email_subject = data.get('subject', '')
        self.first_name = data.get('first_name', '')
        self.email_text = data.get('body', '')
        self.receiver_email = data.get('to', '')
        self.sender_email = os.environ['GMAIL_USER']
        self.password = os.environ['GMAIL_PASSWORD']
        self.send_time = data.get('send_time', '')
        
        
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = self.email_subject
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        
        # Create the plain-text and HTML version of your message
        html = """
            <html><body><p>Hi,</p>
            <p>{first_name}</p> 
            <br/>
            {body}
            <br/>
            <p>Regards,</p>
            <p>Ankit Suwal</p>
            </body></html>
            """.format(first_name=self.first_name, body=self.email_text)
            
        part = MIMEText(html, "html")
        self.message.attach(part)
        
    def send_email(self):
        """
        send an email to receiver email
        Returns:
            _type_: boolean
        """
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, self.message.as_string())
            return True, True
        except smtplib.SMTPResponseException as e:
            raise {"error_code" : e.smtp_code, "error_message" : e.smtp_error, 
                   "message": "SMTP connection faild.", "code": 500}
    
    def send_email_at(self):
        """
        send an eamil at specific time
        """
        time.sleep(self.rem_time)
        return self.send_email()
    
    def email_validation(self):
        self.rem_time = 0
        if self.receiver_email == '':
            return {"message": "Please provide receiver email address.", "code": 400}, False
        if re.fullmatch(email_regex, self.receiver_email) is None:
            return {"message": "Please provide correct email.", "code": 400}, False

        if self.send_time: 
            format = "%Y-%m-%d %H:%M:%S"
            try:
                res = bool(datetime.strptime(self.send_time, format))
            except ValueError:
                res = False
            if res:
                dt_object = datetime.strptime(self.send_time, format)
            else:
                return {"Date should match the format" :format, "code": 401}, False
            
            tz_NY = pytz.timezone('Asia/Kolkata')   
            datetime_NY = datetime.now(tz_NY).replace(tzinfo=None)  

            self.rem_time = dt_object - datetime_NY
            self.rem_time = self.rem_time.total_seconds()
            if self.rem_time < 0:
                return {"message": "You have provided the past date or time, please provide present or future date and time.",
                        "code": 401}, False
        print("self.rem_time: ", self.rem_time)
        if self.rem_time == 0: 
            v1, v2 = self.send_email()
            print("\nv1, v2: ", v1, v2)
        else: 
            v1, v2 = self.send_email_at()
        
        return v1, v2