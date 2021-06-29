# Author: GiangNT
# Desc: Monitor MBMS PRS CLIENT SECURITY.DAT
# Date: 25/06/2021
# pip install pyfiglet

import datetime
import os
import sys
import time
import logging
import json
import requests
from pyfiglet import Figlet

# defining the api-endpoint  
API_ENDPOINT = "https://speaker.vndirect.com.vn/api"

headers = {
    'content-type': 'application/json',
    'x-api-key': '51e2ac2ebd8z9d112af03eb0c82'
}

WAIT1 = 60
WAIT2 = 300

def speaker(message):
    try:
        # data to be sent to api 
        payload = {"message": message, "language":"vn"}
        # sending post request and saving response as response object 
        requests.post(API_ENDPOINT, data = json.dumps(payload), headers=headers)
    except:
        print('[ERROR] Exception occur: ', str(e))
        exit(-1)
        
def last_modified(file_name):   
   statinfo = os.stat(file_name)   
   return statinfo.st_mtime
       
def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

# Trading hours in Morning
morning_start = datetime.time(9, 0, 0)
morning_end = datetime.time(11, 30, 0)

# Trading hours in Afternoon
afternoon_start = datetime.time(13, 0, 0)
afternoon_end = datetime.time(14, 45, 0)

if __name__ == '__main__':
        try:
                custom_fig = Figlet(font='graffiti')
                print(custom_fig.renderText('SECURITY'))
                
                LOG_DIR = os.getcwd()
                #LOG_FILE = LOG_DIR + datetime.datetime.now().strftime("\log_%d%m%Y_%H%M%S.txt")
                LOG_FILE = LOG_DIR + "\log.txt"
                
                logger = logging.getLogger('VND')
                logger.setLevel(logging.INFO)
                
                output_file_handler = logging.FileHandler(LOG_FILE)
                stdout_handler = logging.StreamHandler(sys.stdout)

                logger.addHandler(output_file_handler)
                logger.addHandler(stdout_handler)
                                
                #PROGRAM_NAME = sys.argv[0]                                                                
                #if len(sys.argv) < 2:
                #    print("Missing arguments!!! Usage: python " + PROGRAM_NAME + " [Path to File]")
                #    print("For example: python " + PROGRAM_NAME + " C:\Windows\System32\drivers\etc\hosts")
                #    exit(-1)
                
                #FILE_NAME = sys.argv[1]
                
                ### E:/HOSTC_IS/BACKUP01, E:/HOSTC_IS/BACKUP02 ... E:/HOSTC_IS/BACKUP30
                FOLDER_FORMAT = datetime.datetime.now().strftime("%d")
                FILE_NAME = "E:/HOSTC_IS/BACKUP" + FOLDER_FORMAT + "/SECURITY.DAT"
                
                if not os.path.exists(FILE_NAME):                    
                    print("File " + FILE_NAME + " does not exist")
                    exit(-2)                                    
                print("Monitor file " + FILE_NAME + " is starting now...")       
                
                while True:
                    current = datetime.datetime.now().time()
                    # Check if Trading hour end
                    if (current.hour >= 15):
                        exit(0)
                        
                    # Check if in Trading hours
                    if (time_in_range(morning_start, morning_end, current) or time_in_range(afternoon_start, afternoon_end, current)):
                        LAST_MODIFIED = datetime.datetime.fromtimestamp(last_modified(FILE_NAME))                                
                        time.sleep(WAIT1)
                        LAST_MODIFIED_AFTER = datetime.datetime.fromtimestamp(last_modified(FILE_NAME))
                    
                        if (LAST_MODIFIED == LAST_MODIFIED_AFTER):
                            message = time.strftime("%c") + " WARN: Last modified of File " + FILE_NAME + " is not updated (" + str(LAST_MODIFIED) + ")"
                            logger.info(message)
                            speaker("Anh Hứng Tình ơi, PRS đang không có dữ liệu. Anh kiểm tra ngay nhé")
                            print()
                            time.sleep(WAIT2)
                    else:
                        time.sleep(WAIT2)
                                        
        except Exception as e:
                print('[ERROR] Exception occur: ', str(e))
                exit(-1)

