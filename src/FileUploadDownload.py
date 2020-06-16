import os
import copy
import src.imageclassify as ic
from flask import Flask, jsonify, send_from_directory, render_template, request, session,json
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from werkzeug import secure_filename, FileStorage

# import flask_uploads
# import flask_dropzone
# from flask import CORS, cross_origin

UPLOAD_DIRECTORY = "kaplptreeimages"

api = Flask(__name__)
api.secret_key = ("DG123")
dropzone = Dropzone(api)
# Dropzone settingsapp.config['DROPZONE_UPLOAD_MULTIPLE'] = True
api.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
api.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
api.config['DROPZONE_REDIRECT_VIEW'] = 'results'
destination = ''

# Uploads settings
api.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/kaplptreeimages/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(api, photos)
patch_request_class(api)  # set maximum file size, default is 16MB
file_srces = []
class_output=[None] * 20
class_output_2d=[[None] *2]*10
# CORS(api)
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
api_result_str = ''

# Call factory function to create our blueprint
@api.route('/')
@api.route('/', methods=['GET', 'POST'])
def index():
    # list to hold our uploaded image urls
    # set session for image results

    if "file_srces" not in session:
        session['file_srces'] = []
    # list to hold our uploaded image urls
    # file_srces = session['file_srces']
    if request.method == 'POST':
        file_obj = request.files

        for f in file_obj:
            file = request.files.get(f)
            # save the file with to our photos folder
            target = os.path.join(os.getcwd(), "kaplptreeimages")
            target = os.path.join(target, "uploads")
            print(target)
            if not os.path.isdir(target):
                os.mkdir(target)
            filename = photos.save(file, name=file.filename)
            #filename = photos.save(file)

            print(photos.url(filename))
            #file_srces.append(photos.url(filename))
            destination = os.path.join(target, filename)

            print(file.filename)
            print(destination)
            #file.save(destination)
            # Load API keys
            api_keys={}
            print('before json- api_keys' )
            with open('./api_keys.json') as data_file:
                api_keys= json.loads(data_file.read())

            print(type(api_keys),'- ',api_keys)
            api_result = ic.call_vision_api(destination, api_keys)
            # api_result = ic.call_vision_api(photos.url(filename), api_keys)
            file_srces.append(api_result)
            os.remove(destination)
            api_result_str = json.dumps(api_result, sort_keys=True, indent=4, separators=(',', ': '))
            print(api_result)
            print(api_result["images"])
            classifiers=api_result["images"]
            for clx in classifiers:
                list_classfier=clx["classifiers"]
                print(len(list_classfier))
                for i in range(len(clx["classifiers"])):

                    classes=list_classfier[0].get("classes")
                    print('XXXXDDGGG')

                    class_output_2d=copy.copy(classes)
                    for i in range(len(classes)):
                        class_output[i]= classes[i].get('class') +'  |   '+str(classes[i].get('score')*100)+'%'

                                          #for image_class in jsonData:
             #   print (image_class.get("class"))

            # session['file_srces'] = file_srces
            # return "uploading..."
    # return dropzone template on GET request

    return render_template('index.html')


@api.route('/results')
def results():
    print(" in results")

    # redirect to home if no images to display
    # if "file_srces" not in session or session['file_srces'] == []:
    #    return render_template('index.html')

    # set the file_urls and remove the session variable
    # file_srces = session['file_srces']
    # session.pop('file_srces', None)
    print(*class_output_2d)
    print(*class_output)
    return render_template('success.html', result=file_srces,class_output=[x for x in class_output if x is not None])
    #return render_template('success.html', result=file_srces, class_output=[x for x in class_output_2d if x[0] is not None])

if __name__ == "__main__":
    api.run(host="0.0.0.0")
    #api.run(debug=True, port=5020)
