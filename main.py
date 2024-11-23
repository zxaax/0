"""هذا هو الكود الأساسي لا تقم بالتعديل عليه"""

"""py moa_yad.t.me GitHub@moa-yad"""

import os

import struct

from pyrogram import Client

from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneNumberInvalid,
    AuthKeyUnregistered,
    ApiIdInvalid,
    PhoneNumberFlood,
    PhoneCodeInvalid,
    PasswordHashInvalid,
    PhoneNumberBanned,
    FloodWait,
    PhoneCodeExpired
)

api_id = os.environ.get("apiid")
if api_id is not None and api_id != '':
    print("تم تعيين الأيبي أيدي .")
else:
    print("لم يتم تعيين الأيبي أيدي .")

api_hash = os.environ.get("apihash")
if api_hash is not None and api_hash != '':
    print("تم تعيين الأيبي هاش .")
else:
    print("لم يتم تعيين الأيبي هاش .")

phone = os.environ.get("phone")
if phone is not None and phone != '':
    print("تم تعيين رقم الهاتف .")
else:
    print("لم يتم تعيين رقم الهاتف .")

try:
    client = Client('session', api_id, api_hash)
    is_user_authorized = client.connect()
except AttributeError:
    print('قم بملء المتغيرات بالكامل وبعدها أعد التشغيل .')
    exit()

try:
    if not is_user_authorized:
        send_code = client.send_code(phone)
        try:
            print("تم إرسال رمز التحقق إلى حسابك ،")
            code = input('قم بإدخال رمز التحقق: ')
            client.sign_in(phone, send_code.phone_code_hash, code)
        except PhoneCodeInvalid:
            print('رمز التحقق خطأ،  حاول مرة اخرى .')
            code = input('قم بإدخال رمز التحقق: ')
            client.sign_in(phone, send_code.phone_code_hash, code)
except SessionPasswordNeeded:
    print("!! تم تفعيل التحقق بخطوتين في حسابك مسبقًا !!")
    password = input('قم بإدخال رمز التحقق بخطوتين:  ')
    try:
        client.check_password(password=password)
    except PasswordHashInvalid:
        client.check_password(password=input('الرمز خطأ، حاول مرة أخرى:  '))
except PhoneCodeExpired:
    print('تم انتهاء صلاحية رمز التحقق، قم بطلب واحد جديد .')
except PhoneCodeInvalid:
    print('رمز تسجيل الدخول خطأ، قم بتشغيل الكود مرة أخرى .')
except PasswordHashInvalid:
    print('رمز التحقق بخطوتين خطأ، قم بتشغيل الكود مرة أخرى .')
except PhoneNumberBanned:
    print('رقم الهاتف محظور من التلجرام، قم بالتأكد من صحته.')
except PhoneNumberInvalid:
    print('رقم الهاتف خطأ، قم بتصحيحه وحاول مرة أخرى .')
except PhoneNumberFlood:
    print('عدد كبير من محاولات تسجيل الدخول، حاول بعد 24 ساعة .')
except ApiIdInvalid:
    print('أيبي أيدي/هاش  خطأ، قم بتصحيحهما وحاول مجددًا .')
except FloodWait as e:
    print( f'عدد كبير من محاولات تسجيل الدخول، حاول بعد {e.value} ثانية .')
except Exception as e:
    print(f'خطأ غير معرف: {e}')
try:
    session_string = client.export_session_string()
    client.send_message(
        "me",
        f"**هذا هو كود سيشن بايروجرام الخاص بك**:\n\n`{session_string}`\n\n**لا تشارك هذا الكود مع أي مستخدم !**\n@Tepthon",
        )
    print("تم إنشاء كود السيشن، تم إرساله إلى الرسائل المحفوظة على التلجرام .")
except struct.error:
     print("فشل في إنشاء كود السيشن، حاول مرة أخرى.")

