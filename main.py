"""هذا هو الكود الاساسي لا تقم بالتعديل علية"""

"""py moa_yad.t.me GitHub@moa-yad"""

import requests

import bs4

import sys

app_shortname = sys.argv[1]
phone = sys.argv[2]

try:
    phone_data = {"phone": phone}
    send_code = requests.post("https://my.telegram.org/auth/send_password", data=phone_data).json()["random_hash"]
except:
    print("فشل ارسال رمز التحقق.")
    print("اما رقم الهاتف خطأ ، او عدد كبير من المحاولات .")
    exit()
try:
    code = input("قم بادخال رمز التحقق : ")
    payload = {"phone": phone, "random_hash": send_code, "password": code}
    login_response = requests.post("https://my.telegram.org/auth/login", data=payload)
    if "Invalid confirmation code!" in login_response.text:
        print("الرمز خطأ اعد المحاولة من جديد.")
        code = input("قم بادخال رمز التحقق : ")
        payload = {"phone": phone, "random_hash": send_code, "password": code}
        login_response = requests.post("https://my.telegram.org/auth/login", data=payload)
        if "Invalid confirmation code!" in login_response.text:
            print("رمز التحقق خطأ ، فشل الاستخراج.")
            exit()

except requests.exceptions.RequestException:
    print(f"فشل الاتصال بـ التلجرام .")
    exit()

cookies_dict = login_response.cookies.get_dict()
app = requests.post("https://my.telegram.org/apps", cookies=cookies_dict).text
response = bs4.BeautifulSoup(app, features="html.parser")

if response.title.string == "Create new application":
    print("لم يتم استخراج الايبيات في حسابك من قبل .")
    finding = response.find("input", {"name": "hash"}).get("value")
    AppInfo = {
        "hash": finding,
        "app_title": phone,
        "app_shortname": app_shortname,
        "app_url": "",
        "app_platform": "android",
        "app_desc": ""
    }

    try:
        app = requests.post("https://my.telegram.org/apps/create", data=AppInfo, cookies=cookies_dict).text
        if app != "ERROR":
            print("يتم استخراج الايبيات")
            create_app = requests.get("https://my.telegram.org/apps", cookies=cookies_dict).text
            read_app = bs4.BeautifulSoup(create_app, features="html.parser")
            env = read_app.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
            api_id = env[0].string
            api_hash = env[1].string

            print(f"ايبي-ايدي :{api_id}")
            print(f"ايبي-هاش :{api_hash}")
        else:
            print("حسابك محظور من استخراج الايبيات .")
    except:
        print("فشل الاستخراج خطأ في الاتصال .")

elif response.title.string == "App configuration":
    print("تم انشاء الايبيات في حسابك مسبقاً .")
    env = response.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
    api_id = env[0].string
    api_hash = env[1].string
    print(f"ايبي-ايدي :{api_id}")
    print(f"ايبي-هاش :{api_hash}")

