import imp
import json
import PyPDF2
import traceback
import pandas as pd

from celery_config.tasks import create_task
from flask import Flask, jsonify, request, Response
import base64
from libraries.custom_errors import CustomErrors
from libraries.constants import generic_error_msg
from libraries.response import ApiResponse
class DataExtraction():
    """_summary_
       Check request type and file request 
       transfer the request to asynchronous function for background process.
    """
    def __init__(self, content_type=None):
        self.content_type = content_type
        self.allowed_files_csv = ('csv', 'xlsx')
        self.allowed_files_pdf = ('pdf')

    def check_file(self, file):
        file_name = file.filename
        file_info = file_name.split('.')
        print("@@@@@@@@@@@@@@: ", file_name, file_info)
        type = None
        if (len(file_info) < 2):
            ApiResponse().error("No file was uploaded", 400)
        if file_info[1] and file_info[1] in self.allowed_files_csv:
            type = 'csv'
        elif file_info[1] and file_info[1] in self.allowed_files_pdf:
            type = 'pdf'
        else:
            ApiResponse().error("Please upload only .csv, .xlsx or .pdf files", 400)

        return True, type   
    
    
    def data_extraction(self):
        try:
            print("\ndataextraction"* 3)
            if self.content_type == 'application/xml' or self.content_type == 'text/xml':
                try: 
                    print("You are extracting xml file")
                    # Asynchronous process
                    task = create_task.apply_async(args=[self.content_type, 
                                                         request.get_data().decode('utf8')])
                    return task.task_id, True
                except Exception as e:
                    print("####>>>>: ", traceback.format_exc())
                    return generic_error_msg, False
        
            elif self.content_type == 'application/json':
                try:
                    print("You are extracting JSON file")
                    rbody = request.json
                except Exception as e:
                    print(traceback.format_exc())
                    return "Invalid JSON format", False
                
                data = rbody["data"]
                # Asynchronous process
                task = create_task.apply_async(args=[self.content_type, data]) 
                return task.task_id, True
            
            elif 'file' in request.files:
                print("\n you are in file section." * 3)
                files = request.files.getlist('file')
                resp_ = {}
                for ind, file in enumerate(files):
                    boolvar, type = self.check_file(file)
                    if type == 'csv':
                        data = self.csv_xlsx_extraction(file)
                        resp_['csv_file_' + str(ind)] = data
                    elif type == 'pdf':
                        data = self.pdf_extraction(file)
                        resp_['pdf_file_' + str(ind)] = data
                    else:
                        return "Please upload only .csv, .xlsx or .pdf files.", False
                print("\nresp_: ", resp_)
                return resp_, True
        except Exception as e:
            print(traceback.format_exc())
            return "Error in data_extraction.", False
    
    def csv_xlsx_extraction(self, data):
        print("\nyou are in csv_xlsx_extraction" *3)
        initial_df = pd.read_excel(data, keep_default_na=False)
        str_data = initial_df.to_json()
        task = create_task.apply_async(args=['file', str_data])
        return {"task_id": task.task_id}
    
    def pdf_extraction(self, data):
        print("\nyou are in pdf_extraction" * 3)
        pdfReader = PyPDF2.PdfFileReader(data) # creating a pdf reader object
        # printing number of pages in pdf file
        print("number of pages in pdf file: ", pdfReader.numPages)
        page_data = []
        for i in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(i) # creating a page object
            text = pageObj.extractText()
            page_data.append(text)
        return {"result": page_data}