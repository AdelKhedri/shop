from kavenegar import *

def sendcode(api_key, params):
    api = KavenegarAPI(api_key)
    response = api.sms_send(params)
    print(response)
    # sendcode('', {'sender': '10008663', 'receptor': phone_number, 'message': f'کد ثبت نام :\n {code}'})