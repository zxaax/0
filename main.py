"""هذا هو الكود الأساسي لا تقم بالتعديل عليه"""

"""py moa_yad.t.me GitHub@moa-yad"""

import os

from telethon.sync import TelegramClient

from telethon.errors import (
    SessionPasswordNeededError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberBannedError,
    PhoneNumberInvalidError,
    PhoneNumberFloodError,
    AuthKeyUnregisteredError,
    FloodWaitError,
    ApiIdInvalidError
)

from telethon.sessions import StringSession

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
    client = TelegramClient('session', api_id, api_hash)
    client.connect()
except ValueError:
    print('قم بملء المتغيرات بالكامل وبعدها أعد التشغيل .')
    exit()

try:
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            print("تم إرسال رمز التحقق إلى حسابك ،")
            code = input('قم بإدخال رمز التحقق: ')
            client.sign_in(phone, code)
        except PhoneCodeInvalidError:
            print('رمز التحقق خطأ، حاول مرة أخرى .')
            code = input('قم بإدخال رمز التحقق: ')
            client.sign_in(phone, code)
except SessionPasswordNeededError:
    print("!! تم تفعيل التحقق بخطوتين في حسابك مسبقًا !!")
    password = input('قم بإدخال رمز التحقق بخطوتين:  ')
    try:
        client.sign_in(password=password)
    except PasswordHashInvalidError:
        client.sign_in(password=input('الرمز خطأ، حاول مرة أخرى:  '))
except PhoneCodeExpiredError:
    print('تم انتهاء صلاحية رمز التحقق، قم بطلب واحد جديد .')
except PhoneCodeInvalidError:
    print('رمز تسجيل الدخول خطأ، قم بتشغيل الكود مرة أخرى .')
except PasswordHashInvalidError:
    print('رمز التحقق بخطوتين خطأ، قم بتشغيل الكود مرة أخرى .')
except PhoneNumberBannedError:
    print('رقم الهاتف محظور من التلجرام، قم بالتأكد من صحته.')
except PhoneNumberInvalidError:
    print('رقم الهاتف خطأ، قم بتصحيحه وحاول مرة أخرى .')
except PhoneNumberFloodError:
    print('عدد كبير من محاولات تسجيل الدخول، حاول بعد 24 ساعة .')
except ApiIdInvalidError:
    print('أيبي أيدي/هاش  خطأ ، قم بتصحيحه وحاول مجددًا .')
except FloodWaitError as e:
    print( f'عدد كبير من محاولات تسجيل الدخول، حاول بعد {e.seconds} ثانية .')
except Exception as e:
    print(f'خطأ غير معرف: {e}')
try:
    session_string = StringSession.save(client.session)
    client.send_message(
        "me",
        f"**هذا هو كود سيشن تيليثون الخاص بك**:\n\n`{session_string}`\n\n**لا تشارك هذا الكود مع أي مستخدم !**\n@Tepthon",
        )
    print("تم إنشاء كود السيشن، تم إرساله إلى الرسائل المحفوظة على التلجرام .")
except AuthKeyUnregisteredError:
    print("فشل في إنشاء كود السيشن، حاول مرة أخرى.")
