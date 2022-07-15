# import packages
from crypt import methods
import os
import pytz
import json
import traceback
import pandas as pd
from datetime import datetime

from flask import Flask
from flask import Flask, jsonify, request, Response

from bson.json_util import dumps, loads
from pymongo import MongoClient

# import custome libraries
# from custom_errors import CustomErrors
from libraries.email import Email
from libraries.response import ApiResponse
from libraries.constants import CONTENT_TYPES
from libraries.custom_errors import CustomErrors
from libraries.constants import generic_error_msg
from libraries.data_extraction import DataExtraction
# from libraries.database import db
# celery configuration
from celery_config.tasks import create_task
from celery_config.tasks import celery

app = Flask(__name__)


"""mongo db setup"""
try:
    db_client = MongoClient(host=os.environ['MONGODB_HOSTNAME'],
                            port=int(os.environ['MONGO_PORT']),
                            username=os.environ['MONGO_INITDB_ROOT_USERNAME'],
                            password=os.environ['MONGO_INITDB_ROOT_PASSWORD'],
                            authSource=os.environ['MONGO_AUTH_SOURCE'])
    db = db_client['test-db']
except Exception as err:
    print("Could not connect to MongoDB: ", err)

@app.route('/', methods=['GET'])
def main():
    print("you are in main.")
    return ApiResponse().success("You are in main.", 200)


@app.route('/test', methods=['GET'])
def test():
    print("you are in test.")
    return ApiResponse().success("You are calling test.", 200)
        

@app.route('/functionality', methods=["GET", "POST"])
def functionality():
    """_summary_
    Returns:
        _type_: dict, task id and email successful message
    """
    try:
        content_type = request.content_type
        args = request.args.get('request_type', '')
        print("\n request.content_type: ", request.content_type)
        print("\n request.files: ", request.files)
        print("\n args: ", args)
        if content_type in ['application/xml', 'text/xml', 'application/json'] and args == '':
           print("\n11111111111111" * 3)
           task, bool_value = DataExtraction(content_type).data_extraction()
           if bool_value:
                return ApiResponse().success(task, 200)
           else: 
               return ApiResponse().error(task, 404)
        
        elif 'file' in request.files:
            print("\n22222222222222" * 3)
            task, bool_value = DataExtraction(content_type).data_extraction()
            if bool_value:
                return ApiResponse().success(task, 200)
            else: 
               return ApiResponse().error(task, 404)

        elif args == 'email':
            print("\n3333333333333" * 3)
            format = "%Y-%m-%d %H:%M:%S"
            try:
                try:
                    data = request.json
                except Exception as err:
                    return ApiResponse().error("Invalid JSON format.", 404)

                if data == {}:
                    return ApiResponse().error("Please provide valid.", 404)

                value, val_bool = Email(data).email_validation()
                if not val_bool:
                    return value
                email_data = {
                    "receiver_email": data.get('to', ''),
                    "send_time": data.get('send_time', '') if data.get('send_time', '') != '' else datetime.now().strftime(format),
                    "created_date": datetime.now().strftime(format)
                }
                if val_bool:
                    email_data["status"] = "Success"
                    print("email_status: ", email_data)
                    db.email_status.insert_one(email_data)
                    return ApiResponse().success("Email sent successfully.", 200)
                else:
                    email_data["status"] = "Faild"
                    print("email_status: ", email_data)
                    db.email_status.insert_one(email_data)
                    return ApiResponse().error("Sending email process faild.", 401)

            except Exception as err:
                print(traceback.format_exc())
                return ApiResponse().error("Something went wrong.", 404)
        else:
            return ApiResponse().error("Only XML, JSON content, File upload and email are supported",
                                       404)
            
    except Exception as err:
        return ApiResponse().error(generic_error_msg, 404)


@app.route('/task_status/<task_id>', methods=['GET'])
def get_status(task_id):
    try:
        task_result = celery.AsyncResult(task_id, app=celery)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return ApiResponse().success(result, 200)
    except Exception as e:
        return ApiResponse().error("Task result is failed.", 404)


@app.route("/email_status", methods=["GET"])
def email_status():
    try:
        data = request.json
    except Exception as err:
        return ApiResponse().error("Invalid JSON.", 404)
    
    status = db.email_status.find({"receiver_email": data.get('email', '')})
    if status:
        json_data = dumps(list(status)).replace('\"', "")
        return ApiResponse().success(json_data, 200)
    else:
        return ApiResponse().success("Eamil not found.", 200) 