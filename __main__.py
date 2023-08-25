import os
import time
from datetime import datetime

# Import Firebase Database admin
import firebase_admin
from firebase_admin import credentials

import BusAPI
import RestaAPI

# Fetch the service account key JSON file contents
FBKEY = os.getenv("CertificateKey")
FBURL = os.getenv("FirebaseURL")
cred = credentials.Certificate(FBKEY)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {'databaseURL': FBURL})

# 20초 마다 업데이트
while True:
    RestaAPI.updateRestaurant()
    print("Updated RestaurantAPI")
    BusAPI.getBusesToUniv(37050)
    print("Updated BusAPI")
    print(datetime.now())
    print("------------------------")
    time.sleep(20)
