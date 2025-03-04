# 🔥 FCM HTTP v1 API Migration Helper Python

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Firebase](https://img.shields.io/badge/Firebase-Admin%20SDK-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

Aplikasi ini dibuat untuk membantu migrasi dari **FCM Legacy API** (HTTP dan XMPP) ke **FCM HTTP v1 API**. Dengan menggunakan API ini, Anda dapat mengirim notifikasi melalui FCM dengan mudah, aman, dan terintegrasi dengan Firebase Authentication.

---

## 🚀 **Latar Belakang**

FCM (Firebase Cloud Messaging) telah menghentikan dukungan untuk API lama (HTTP dan XMPP) dan mengharuskan semua aplikasi untuk bermigrasi ke **HTTP v1 API**. Proyek ini menyediakan solusi untuk:

1. **Mengirim notifikasi** menggunakan FCM HTTP v1 API.
2. **Mengamankan API** dengan Firebase Authentication.
3. **Memudahkan integrasi** dengan aplikasi client (Java, Android, dll).

---

## ✨ **Fitur Utama**

- **Mengirim Notifikasi**: Mengirim notifikasi ke perangkat menggunakan FCM HTTP v1 API.
- **Firebase Auth Integration**: Menggunakan `UserId` dari Firebase Auth untuk mengamankan API.
- **Customizable**: Dukungan untuk title, body, gambar, dan data tambahan.
- **Scalable**: Dibangun dengan Flask, mudah untuk di-deploy dan di-scale.

---

## 🛠️ **Teknologi yang Digunakan**

- **Python 3.8+**
- **Flask**: Framework untuk membangun API REST.
- **Firebase Admin SDK**: Untuk validasi `UserId` dan integrasi dengan Firebase Auth.
- **Google Auth Library**: Untuk otentikasi dengan FCM HTTP v1 API.
- **OkHttp** (Java Client): Contoh implementasi client untuk mengirim request ke API.

---

## 🚀 **Cara Menggunakan**

### **1. Persyaratan**

- Python 3.8+
- Firebase Project dengan FCM diaktifkan.
- File Service Account untuk FCM (`service-account-file.json`).

### **2. Instalasi**

1. Clone repositori ini:
   ```bash
   https://github.com/okidesu19/FCM-API-Migration-python.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Letakkan file `firebase-admin-sdk.json` dan `service-account-file.json` di direktori proyek.

4. Jalankan server:
   ```bash
   python fcm_api.py
   ```

   Server akan berjalan di `http://localhost:5000`.

### **3. Mengirim Notifikasi**

#### **Request**:
- **Endpoint**: `POST /send-notification`
- **Headers**:
  ```
  Authorization: Bearer <FIREBASE_AUTH_USER_ID>
  Content-Type: application/json
  ```
- **Body**:
  ```json
  {
    "token": "DEVICE_FCM_TOKEN",
    "title": "Jonathan",
    "body": "Hai, apa kabar?",
    "image_url": "https://example.com/profile.jpg",
    "data": {
        "userId": "12345",
        "chatId": "67890"
    }
  }
  ```

#### **Response**:
- **Berhasil**:
  ```json
  {
    "success": true,
    "message": "Notification sent successfully",
    "response": {
      "name": "projects/YOUR_PROJECT_ID/messages/MESSAGE_ID"
    }
  }
  ```
- **Gagal**:
  ```json
  {
    "success": false,
    "message": "Error message"
  }
  ```

---

## 🔒 **Keamanan**

API ini menggunakan **Firebase Authentication** untuk memvalidasi `UserId`. Pastikan:
1. Hanya pengguna yang terautentikasi yang dapat mengakses API.
2. Gunakan HTTPS untuk mengamankan komunikasi antara client dan server.

---

## 🌟 **Contoh Implementasi Client**

### **Java (OkHttp)**

```java
import okhttp3.*;

public class Main {
  public static void main(String[] args) {
    String json = "{"
                + "\"token\": \"DEVICE_FCM_TOKEN\","
                + "\"title\": \"John Doe\","
                + "\"body\": \"Hai, apa kabar?\","
                + "\"image_url\": \"https://example.com/profile.jpg\","
                + "\"data\": {"
                + "    \"userId\": \"12345\","
                + "    \"chatId\": \"67890\""
                + "}"
                + "}";
    
    String userId = "FIREBASE_AUTH_USER_ID";
    
    new Thread(() -> {
      try {
        OkHttpClient client = new OkHttpClient();
        MediaType JSON = MediaType.parse("application/json; charset=utf-8");
        RequestBody body = RequestBody.create(json, JSON);
        Request request = new Request.Builder()
                .url("http://localhost:5000/send-notification")
                .post(body)
                .addHeader("Authorization", "Bearer " + userId)
                .build();
        try (Response response = client.newCall(request).execute()) {
            System.out.println(response.body().string());
        } catch (Exception e) {
            e.printStackTrace();
        }
      } catch (Exception e) {
        new Handler(Looper.getMainLooper()).post(() -> {
          //...
        });
      }
    }).start();
  }
}
```
**Json**
  ```json
  {
    "token": "DEVICE_FCM_TOKEN",
    "title": "...",
    "body": "...",
    "image_url": "...jpg"
    "data": {
      //data tambahan
      "type": "chat",
      ...
      ...
      ...
      ...
    }
  }
  ```
---

## 📜 **Lisensi**

Proyek ini dilisensikan di bawah **MIT License**. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

---

Dibuat dengan ❤️ oleh Jonathan.  
💡 **Terinspirasi oleh kebutuhan migrasi FCM HTTP v1 API**.
---
