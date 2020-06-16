__author__ = 'Dibya Ganguly'

import json

from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException



def call_vision_api(image_filename, api_keys):
    print('Inside Ic')

    authenticator = IAMAuthenticator(api_keys['ibm'])
    visual_recognition = VisualRecognitionV3(
        version='2020-06-05',
        authenticator=authenticator
    )

    visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com')
    visual_recognition.set_disable_ssl_verification(False)
    #api_keys['ibm']=g5Vkv58GxP4tUhVrMex5jQMKLMHR1qbQx6rTV3h9rth9
#    api_key = api_keys['ibm']

    # Via example found here:
    # https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/visual_recognition_v3.py
    print('Inside Ic key is passed')
   # visual_recognition = VisualRecognitionV3('2020-06-05', api_key={"g5Vkv58GxP4tUhVrMex5jQMKLMHR1qbQx6rTV3h9rth9"})
    print('Inside Ic key passed')
    with open(image_filename, 'rb') as image_file:
        print('opened file - ',image_file)
        #result = visual_recognition.classify(images_file=image_file)
        try:
         classes = visual_recognition.classify(
            images_file=image_file,
            threshold='0.6',
            owners=["me"]
         ,classifier_ids='default').get_result()
         #print(json.dumps(classes, indent=2))
        except ApiException as ex:
            print ("Method failed with status code " + str(ex.code) + ": " + str(ex.message))
            return  'Failed'
        print('opened file result returned')
    return classes


def get_standardized_result(api_result):
    output = {
        'tags' : [],
    }

    api_result = api_result["images"][0]

    if "error" in api_result:
        # Check for error
        output['tags'].append(("error-file-bigger-than-2mb", None))
    else:
        api_result = api_result["classifiers"][0]
        for tag_data in api_result['classes']:
            output['tags'].append((tag_data['class'], tag_data['score']))

    return output



