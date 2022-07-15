import json
import PyPDF2
import traceback
import xmltodict
import pandas as pd
from celery import Celery
from libraries.custom_errors import CustomErrors
import time
generic_error_msg = "Something went wrong"

celery = Celery(broker='redis://localhost:6379/0', backend="amqp", )


@celery.task(bind=True, name="create_task", serializer="json")
def create_task(self, content_type, data=None):
    print("\ncreat_taskk triggred." * 3)
    resp = {}
    try:
        if content_type == 'application/xml' or content_type == 'text/xml':
            req_data = data.encode('utf8')
            time.sleep(300)
            resp["data"] = xmltodict.parse(req_data)
            resp["status"], resp["code"] = "success", 200     
        
        elif content_type == 'application/json':
            resp['data'] = data       
            resp["status"], resp["code"] = "success", 200     
        
        elif content_type == 'file':
            resp['data'] = json.loads(data)
            resp["status"], resp["code"] = "success", 200

        return resp
    except Exception as e:
        print(traceback.format_exc())
        raise CustomErrors(traceback.format_exc(), "Error in create_task", 401)
