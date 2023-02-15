import json
import logging
import pyrebase
import os
import requests
from firebase_admin.auth import ExpiredIdTokenError
from config import firebase_creds_folder
from firebase_admin import auth
import traceback


pb = pyrebase.initialize_app(json.load(open(os.path.join(firebase_creds_folder, 'fbconfig.json'))))

with open(os.path.join(firebase_creds_folder, 'fbconfig.json')) as f:
    d = json.load(f)

FIREBASE_WEB_API_KEY = d['apiKey']
rest_api_url_email_verification = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
rest_api_url_token_refresh = "https://securetoken.googleapis.com/v1/token"
rest_api_url_change_password = "https://identitytoolkit.googleapis.com/v1/accounts:update"
rest_api_url_change_email = "https://identitytoolkit.googleapis.com/v1/accounts:update"


def sign_in_with_email_and_password(email, password):
    user = pb.auth().sign_in_with_email_and_password(email, password)
    return user


def add_user_to_firebase(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return 'Success', user.uid
    except Exception as exp:
        if str(exp).__contains__('INVALID_EMAIL') or str(exp).__contains__("Malformed email address string"):
            return 'Invalid email', None
        else:
            return 'Unexpected error', None


def send_email_verification_by_token(id_token):
    payload = json.dumps({
        "requestType": "VERIFY_EMAIL",
        "idToken": id_token
    })

    r = requests.post(rest_api_url_email_verification,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)
    result = r.json()
    if 'error' in result:
        return False
    return True


def send_email_verification_by_email_and_password(email, password):
    user = sign_in_with_email_and_password(email, password)
    res = send_email_verification_by_token(user['idToken'])
    return res


def verify_token(token, email, refresh_token):
    try:
        decoded_token = auth.verify_id_token(token)
        return email == decoded_token['firebase']['identities']['email'][0], None, decoded_token['email_verified']
    except ExpiredIdTokenError as ex:
        data = get_token_by_refresh_token(refresh_token)
        decoded_token = auth.verify_id_token(data['user_token'])
        return email == decoded_token['firebase']['identities']['email'][0], data, decoded_token['email_verified']


def check_email_verification(email):
    return auth.get_user_by_email(email).email_verified


def get_token_by_refresh_token(refresh_token: str):
    payload = json.dumps({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })

    r = requests.post(rest_api_url_token_refresh,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)
    result = r.json()
    if 'error' in result:
        return None
    return {'refresh_token' : result['refresh_token'], 'user_token': result['access_token']}


def change_password(user_token, new_password):
    payload = json.dumps({
        "idToken": user_token,
        "password": new_password,
        "returnSecureToken": True
    })

    r = requests.post(rest_api_url_change_password,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)
    result = r.json()
    return {'refresh_token': result['refreshToken'], 'user_token': result['idToken']}


def change_email(user_token, new_email):
    payload = json.dumps({
        "idToken": user_token,
        "email": new_email,
        "returnSecureToken": True
    })

    r = requests.post(rest_api_url_change_email,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)
    result = r.json()
    if 'error' in result:
        if result['error']['message'] == 'INVALID_EMAIL':
            return 'Invalid email'
        elif result['error']['message'] == 'EMAIL_EXISTS':
            return 'Email exists'
        else:
            return 'Unknown error'
    else:
        return {'refresh_token': result['refreshToken'], 'user_token': result['idToken']}