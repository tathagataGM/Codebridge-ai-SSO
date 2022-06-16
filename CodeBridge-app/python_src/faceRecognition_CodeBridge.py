# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 01:47:54 2022
-
"""

import face_recognition
known_image = face_recognition.load_image_file("images/1544209.jpg")
unknown_image = face_recognition.load_image_file("Unknown_images/1655320002.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding,tolerance=0.5)


print(results[0])
