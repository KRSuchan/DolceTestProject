# Import Firebase Database admin
import firebase_admin
# Import URL Request
import requests
from bs4 import BeautifulSoup
from firebase_admin import credentials, db
import time


def updateRestaurant():
    url = 'https://www.kumoh.ac.kr/ko/restaurant02.do'

    try:
        response = requests.get(url)
    except Exception as e:
        print("occured Exception : ", e)
        time.sleep(5)
        response = requests.get(url)

    lunch = []
    dinner = []

    # Web Crawlling
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        for i in range(1, 8):
            # Professor Restaurant lunch Web Parser
            menu = soup.select_one(
                '#jwxe_main_content > div.ko > div > div.menu-list-box > div > table > tbody > tr:nth-child(1) > td:nth-child(' +
                str(i)+') > ul'
            )
            lunch.append(str(menu.get_text()))
            # Professor Restaurant Web Parser
            menu = soup.select_one(
                '#jwxe_main_content > div.ko > div > div.menu-list-box > div > table > tbody > tr:nth-child(2) > td:nth-child(' +
                str(i)+') > ul'
            )
            dinner.append(str(menu.get_text()))

    else:
        print(response.status_code)

    # Update on Firebase Realtime Database
    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('')
    prof_rest = ref.child('prof_menu')

    prof_rest.update({
        '월요일': {
            '중식': lunch[0],
            '석식': dinner[0]
        },
        '화요일': {
            '중식': lunch[1],
            '석식': dinner[1]
        },
        '수요일': {
            '중식': lunch[2],
            '석식': dinner[2]
        },
        '목요일': {
            '중식': lunch[3],
            '석식': dinner[3]
        },
        '금요일': {
            '중식': lunch[4],
            '석식': dinner[4]
        },
        '토요일': {
            '중식': lunch[5],
            '석식': dinner[5]
        },
        '일요일': {
            '중식': lunch[6],
            '석식': dinner[6]
        }
    })
