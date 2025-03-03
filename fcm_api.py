from flask import Flask, request, jsonify
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import firebase_admin
from firebase_admin import auth, credentials
import os
import json

app = Flask(__name__)

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Inisialisasi FCM Service
class FCMService:
  def __init__(self, credentials_path):
    self.credentials_path = credentials_path
    self.project_id = self._get_project_id()
    self.session = self._create_authorized_session()
  
  def _get_project_id(self):
    with open(self.credentials_path, 'r') as f:
      credentials = json.load(f)
      return credentials['project_id']
  
  def _create_authorized_session(self):
    scopes = ['https://www.googleapis.com/auth/firebase.messaging']
    credentials = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
    return AuthorizedSession(credentials)
  
  def send_notification(self, token, title, body, image_url=None, data=None):
    url = f'https://fcm.googleapis.com/v1/projects/{self.project_id}/messages:send'
    message = {
      "message": {
        "token": token,
        "notification": {
          "title": title,
          "body": body,
          "image": image_url
        },
        "data": data or {}
      }
    }
    response = self.session.post(url, json=message)
    return response.json()


# Inisialisasi FCM Service dengan file service account
fcm_service = FCMService('serviceAccountKey.json')

# Middleware untuk validasi Authorization Header
def validate_user_id(user_id):
  try:
    # Verifikasi UserId menggunakan Firebase Admin SDK
    user = auth.get_user(user_id)
    return user is not None
  except Exception as e:
    print(f"Error validating user: {e}")
    return False


@app.route('/send-notification', methods=['POST'])
def send_notification():
    try:
      # Ambil Authorization Header
      auth_header = request.headers.get('Authorization')
      if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
          "success": False,
          "message": "Authorization header is missing or invalid"
        }), 401
      
      # Ekstrak UserId dari header
      user_id = auth_header.split('Bearer ')[1]
      
      # Validasi UserId
      if not validate_user_id(user_id):
        return jsonify({
          "success": False,
          "message": "Invalid UserId"
        }), 403
      
      # Ambil data dari request JSON
      data = request.json
      token = data.get('token')
      title = data.get('title')
      body = data.get('body')
      image_url = data.get('image_url')
      custom_data = data.get('data', {})
      
      # Kirim notifikasi ke FCM
      response = fcm_service.send_notification(
        token=token,
        title=title,
        body=body,
        image_url=image_url,
        data=custom_data
      )
      
      # Berikan respons ke client
      return jsonify({
        "success": True,
        "message": "Notification sent successfully",
        "response": response
      }), 200
    except Exception as e:
      return jsonify({
        "success": False,
        "message": str(e)
      }), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)