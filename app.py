from flask import Flask, jsonify, request
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_uid(person_link):
    if 'profile.php?id=' in person_link:
        uid = person_link.split('?id=')[1]
        return uid
    else:
        burp0_url = "https://fbuid.net:443/home/get_uid"
        burp0_cookies = {"PHPSESSID": "a2jrmvsflmfdlrn4f4gf1gnps7"}
        burp0_headers = {"Connection": "close", "sec-ch-ua": "\"Chromium\";v=\"91\", \" Not;A Brand\";v=\"99\"",
                         "Accept": "*/*", "X-Requested-With": "XMLHttpRequest", "sec-ch-ua-mobile": "?0",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                         "Origin": "https://fbuid.net", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors",
                         "Sec-Fetch-Dest": "empty", "Referer": "https://fbuid.net/", "Accept-Encoding": "gzip, deflate",
                         "Accept-Language": "en-US,en;q=0.9"}
        burp0_data = {"url": person_link}
        try:
            r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, timeout=20)
            print(r.text)
            if r.status_code == 200 and json.loads(r.content.decode('utf-8-sig'))['status'] == "success":
                return json.loads(r.content.decode('utf-8-sig'))['uid']
            else:
                return None
        except Exception as e:
            return None


def get_uid_second(person_link):
    url = 'https://api.findids.net/api/get-uid-from-username'
    if 'profile.php?id=' in person_link:
        uid = person_link.split('?id=')[1]
        return uid
    else:
        username = person_link.strip("/").split('facebook.com/')[1]
        datas = {"username": username}
        try:
            r = requests.post(url, data=datas, timeout=20)
            if r.json()['status'] == 200 and r.json()['success'] == True:
                return r.json()['data']['id']
            else:
                return None
        except Exception as e:
            return None


def get_uid_three(linkFacebook):
    if 'profile.php?id=' in linkFacebook:
        uid = linkFacebook.split('?id=')[1]
        return uid
    else:
        url = 'https://id.atpsoftware.vn'
        data = {
            'linkCheckUid': linkFacebook
        }
        headers = {"Connection": "close", "Cache-Control": "max-age=0",
                   "sec-ch-ua": "\"Chromium\";v=\"91\", \" Not;A Brand\";v=\"99\"", "sec-ch-ua-mobile": "?0",
                   "Upgrade-Insecure-Requests": "1", "Origin": "https://id.atpsoftware.vn",
                   "Content-Type": "application/x-www-form-urlencoded",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                   "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                   "Sec-Fetch-Dest": "document", "Referer": "https://id.atpsoftware.vn/",
                   "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}

        try:
            data = requests.post(url, data=data, verify=False, timeout=20, headers=headers).text
            return data.split('center;overflow: hidden;">')[1].split('<')[0]
        except Exception as e:
            return None


def get_uid_four(linkFacebook):
    if 'profile.php?id=' in linkFacebook:
        uid = linkFacebook.split('?id=')[1]
        return uid
    else:
        burp0_url = "https://getinfofb.com:443/check.php"
        burp0_cookies = {"PHPSESSID": "diuij959omg77o506qs9n80bds"}
        burp0_headers = {"Sec-Ch-Ua": "\";Not A Brand\";v=\"99\", \"Chromium\";v=\"94\"", "Accept": "*/*",
                         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                         "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                         "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://getinfofb.com",
                         "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
                         "Referer": "https://getinfofb.com/", "Accept-Encoding": "gzip, deflate",
                         "Accept-Language": "en-US,en;q=0.9"}
        burp0_data = {"url": linkFacebook}
        try:
            r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, timeout=20)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                uid = str(soup.find('input', {'name': 'Uid'})['value']).split('Uid: ')[1]
                return uid
            else:
                return None
        except Exception as e:
            return None


@app.route("/get_uid", methods=["POST"])
def setName():
    if request.method == 'POST':
        posted_data = request.get_json()
        personal_url = posted_data['link_fb']
        uid = get_uid(personal_url)
        return {'uid': uid}, 200


@app.route("/get_uid_2", methods=["POST"])
def setUID():
    if request.method == 'POST':
        posted_data = request.get_json()
        personal_url = posted_data['link_fb']
        uid = get_uid_second(personal_url)
        return {'uid': uid}, 200


@app.route("/get_uid_3", methods=["POST"])
def setUID3():
    if request.method == 'POST':
        posted_data = request.get_json()
        personal_url = posted_data['link_fb']
        uid = get_uid_three(personal_url)
        return {'uid': uid}, 200


@app.route("/get_uid_4", methods=["POST"])
def setUID2():
    if request.method == 'POST':
        posted_data = request.get_json()
        personal_url = posted_data['link_fb']
        uid = get_uid_four(personal_url)
        return {'uid': uid}, 200


@app.route('/')
def index():
    return 'hello campain!'


if __name__ == '__main__':
    app.run()
