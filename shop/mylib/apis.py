from kavenegar import *

def sendcode(api_key, params):
    api = KavenegarAPI(api_key)
    response = api.sms_send(params)
    print(response)