import pyrebase
import requests
from datetime import datetime


# Firebase yapılandırma bilgilerini burada girin
config = {
    "apiKey": "AIzaSyBj6r8qK30L7NTspBnR-XJV8HKSN5KjJt8",
    "authDomain": "ekmek-sayaci.firebaseapp.com",
    "databaseURL": "https://ekmek-sayaci-default-rtdb.firebaseio.com/",  # Doğru URL
    "projectId": "ekmek-sayaci",
    "storageBucket": "ekmek-sayaci.appspot.com",
    "messagingSenderId": "762075188413",
    "appId": "1:762075188413:android:6b783fdffdac4031557bd4"
}

# Firebase'i başlat
firebase = pyrebase.initialize_app(config)

# Veritabanı referansını al
db = firebase.database()

dogrumu = None

# İşlem kaydetme fonksiyonu
def islem_kaydet(kullanici, islem_turu, miktar):
    try:
        # İşlem verisini oluştur
        islem_verisi = {
            "kullanici": kullanici,
            "islem_turu": islem_turu,
            "miktari": miktar,
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # İşlemi Firebase'e ekle
        db.child("islemler").push(islem_verisi)
        print("İşlem başarıyla kaydedildi:", islem_verisi)
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Tüm işlemleri çekme fonksiyonu
def tum_islemleri_getir():
    try:
        islemler = db.child("islemler").get()  # Firebase'den işlemleri al
        return islemler.each()  # İşlemleri döndür
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []

# Kullanıcı eklemek için bir fonksiyon
def add_user(user_id, user_data):
    try:
        response = db.child("users").child(user_id).set(user_data)
        print("Kullanıcı başarıyla eklendi:", response)
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Çözümleme Hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def generate_user_id():
    users = db.child("users").get()  # Tüm kullanıcıları al
    if users.each():
        # Mevcut kullanıcı sayısına göre bir ID oluştur
        return str(len(users.each()) + 1)  # Mevcut kullanıcı sayısına 1 ekleyin
    return "1"  # Eğer hiç kullanıcı yoksa ID'yi "1" olarak belirleyin

def kullanici_ekle(isim, sifre):
    user_id = generate_user_id()  # Yeni kullanıcı ID'sini oluştur
    user_data = {
        "name": isim,
        "password": sifre
    }
    # Kullanıcıyı ekle
    add_user(user_id, user_data)

def dogrulama(isim, sifre):
    global dogrumu
    try:
        users = db.child("users").get()  # Kullanıcı verilerini al
        if not users.each():  # Eğer kullanıcı yoksa
            dogrumu = False
            return False

        for user in users.each():

            user_data = user.val()

            if user_data is None:  # Eğer user_data None ise
                continue  # Bir sonraki kullanıcıya geç

            # Kullanıcı adını kontrol et
            if 'name' in user_data and user_data['name'] == isim:
                # Şifreyi kontrol et
                if 'password' in user_data and user_data['password'] == sifre:
                    dogrumu = True  # Doğru giriş
                    
                    return True
                else:
                    dogrumu = False  # Hatalı şifre
                    
                    return False
        dogrumu = False
        return False
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return False
    


# Sayaç oluşturma
def initialize_counter():
    try:
        # "sayaç" adında bir düğüm oluştur ve değerini 0 olarak ayarla
        db.child("sayaç").set(0)
        print("Sayaç başarıyla oluşturuldu.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Sayaç değerini al
def get_counter_value():
    try:
        counter_value = db.child("sayaç").get()
        return counter_value.val()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None

# Sayaçta toplama işlemi yap
def increment_counter(amount):
    try:
        current_value = get_counter_value()
        if current_value is not None:
            new_value = current_value + amount
            db.child("sayaç").set(new_value)
            print(f"Sayaç güncellendi: {new_value}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Sayaçta çıkarma işlemi yap
def decrement_counter(amount):
    try:
        current_value = get_counter_value()
        if current_value is not None:
            new_value = current_value - amount
            db.child("sayaç").set(new_value)
            print(f"Sayaç güncellendi: {new_value}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
