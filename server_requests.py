import requests
import os

URL = os.environ['SERVER_URL']
PI_ID = os.environ['PI_ID']

def motionDetectedRequest():
    res = requests.get(URL + '/detected/' + PI_ID)
    return res

def buttonFeedbackRequest(classification):
    if classification in ['Trash', 'Recycle', 'Compost']:
        res = requests.get(URL + '/feedback/' + PI_ID + '?classification=' + classification)
        return res

# motionDetectedRequest()
