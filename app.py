from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)



def get_uid(person_link):
    if 'profile.php?id=' in person_link:
        uid = person_link.split('?id=')[1]
        return uid
    else:
        burp0_url = "https://fbuid.net:443/home/get_uid"
        burp0_cookies = {"PHPSESSID": "a2jrmvsflmfdlrn4f4gf1gnps7"}
        burp0_headers = {"Connection": "close", "sec-ch-ua": "\"Chromium\";v=\"91\", \" Not;A Brand\";v=\"99\"", "Accept": "*/*", "X-Requested-With": "XMLHttpRequest", "sec-ch-ua-mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": "https://fbuid.net", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://fbuid.net/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
        burp0_data = {"url": person_link}
        try:
            r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, timeout=20)
            if r.status_code == 200 and json.loads(r.content.decode('utf-8-sig'))['status'] == "success":
                return json.loads(r.content.decode('utf-8-sig'))['uid']
            else:
                return None
        except Exception as e:
            return None

@app.route("/get_uid", methods=["POST"])
def setName():
    if request.method=='POST':
        posted_data = request.get_json()
        personal_url = posted_data['link_fb']
        uid = get_uid(personal_url)
        return {'uid':uid}, 200

@app.route('/')
def index():
    return 'hello campain!'


if __name__ == '__main__':
    app.run()
