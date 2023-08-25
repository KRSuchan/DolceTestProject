import json
import os

import requests
from bs4 import BeautifulSoup
from firebase_admin import db


def getBusesToUniv(cityCode):
    resultDict = {
        "bus": []
    }
    routeNo = []
    arrPrevStationCnt = []
    APIKEY = os.getenv("BusAPIKEY")
    # BUS API json 파일 획득
    url = 'https://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList?'
    url += "serviceKey="+APIKEY + \
        "&pageNo=1&numOfRows=10&_type=json&cityCode=" + \
        str(cityCode)+"&nodeId=GMB132"

    print("start to access bus data api")
    response = requests.get(url)

    # response의 json 파일 contents 확인
    print(response.json())
    jsonData = response.json().get('response')
    jsonHeader = jsonData.get('header')
    jsonBody = jsonData.get('body')

    # 서버 상태 코드와 resultCode가 정상일 경우
    if (response.status_code == 200 and jsonHeader.get('resultCode') == "00"):
        # json 파일에서 tag 접근
        busCnt = jsonBody.get('totalCount')
        jsonBody = jsonBody.get('items').get('item')
        # 나온 버스 개수만큼 버스 번호, 남은 정류장 수 획득
        for i in range(0, busCnt):
            arrPrevStationCnt.append(jsonBody[i].get('arrprevstationcnt'))
            routeNo.append(jsonBody[i].get('routeno'))
            resultDict["bus"].append({"routeno": routeNo[i],
                                      "arrprevstationcnt": arrPrevStationCnt[i]})
        print(resultDict)
    # 서버 상태코드나 resultCode가 비정상일 경우 : 500같은 경우
    else:
        print(jsonHeader.get('resultMsg'))
        print(response.status_code)

    # Update on Firebase Realtime Database
    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('')
    busToKIT = ref.child('busToKIT')
    busToKIT.set(resultDict)


def getCityCode():
    url = ''


def updateFirebase():
    url = ''
