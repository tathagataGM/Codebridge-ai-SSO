# -*- coding: utf-8 -*-
import os
import face_recognition

from flask import *
import cv2
import json
import numpy as np
from flask_cors import CORS

import base64
from datetime import datetime
from tkinter import *  
from tkinter import messagebox  
  

#graph = tf.get_default_graph()

app = Flask(__name__)
CORS(app)


def img_to_encoding(path):
  img1 = face_recognition.load_image_file(path)
  embedding = face_recognition.face_encodings(img1)[0]
  return embedding


identity = "demo"
database = {}


def write_into_dict(name,path):
    database[str(name)] = str(path)

def who_is_it(image_path, database):
    
    encoding = img_to_encoding(image_path)
    min_dist = False
    # Loop over the database dictionary's names and encodings.
    for name , location in database.items(): 
        dist = face_recognition.compare_faces([img_to_encoding(location)],encoding,tolerance=0.4)
        
        if dist[0] ==True:
            min_dist = dist[0]
            identity = name
    if min_dist == False:
        print("Not in the database.")
    else:
        print ("it's " + str(identity) + "  " + str(min_dist))
    return min_dist, identity
    

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.get_json()['username']
        img_data = request.get_json()['image64']
        path = 'images/'+username+'.jpg'
        with open(path, "wb") as fh:
            fh.write(base64.b64decode(img_data[22:]))
        
        write_into_dict(username,path)
        
        return json.dumps({"status": 200})
    except:
        return json.dumps({"status": 500})



@app.route('/verify', methods=['POST'])
def verify():
    try:
        img_data = request.get_json()['image64']
        img_name = str(int(datetime.timestamp(datetime.now())))    
        
        with open('Unknown_images/'+img_name+'.jpg', "wb") as fh:
            fh.write(base64.b64decode(img_data[22:]))
        path = 'Unknown_images/'+img_name+'.jpg'
        
        min_dist, identity = who_is_it(path, database)
        os.remove(path)
      
        if min_dist == False:
            return json.dumps({"identity": 0})
        return json.dumps({"identity": str(identity)})
        #return json.dumps({"identity": "test2"})
    except:
        return json.dumps({"status": 500})

if __name__ == "__main__":
   
    app.run(debug=True)