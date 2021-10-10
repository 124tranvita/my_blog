# user/pics_handler.py
import os 
from flask import current_app
from PIL import Image

def process_upload_image(upload_image, username):
    '''
    1. upload_image is a return value of FileFiled (value is an instance/Object of class)
    2. upload_image.filename: Get file name of upload picture by get 'filename' variable
    3. Get upload picture extension (*.extention) by split the file name by '.' then take the last value
    4. Naming the file to new format "username + file_extention"
    5. Set the path to save the upload picture
    6. Set the size of picture after process with Image()
    7. Use Image.open() to open upload picture
    8. Take the thumnail by Image.thumnail()
    9. Save upload picture to folder by Image.save()
    -> Complete upload image to server
    10. Set the return value as new name format "username + file_extention" to store in database
    '''
    file_name = upload_image.filename
    file_extension = file_name.split('.')[-1]
    file_rename = str(username) + '.' + file_extension
    save_path = os.path.join(current_app.root_path, 'static\profile_pics', file_rename)

    load_image = Image.open(upload_image)
    load_image.thumbnail([150,150])
    load_image.save(save_path)

    return file_rename



