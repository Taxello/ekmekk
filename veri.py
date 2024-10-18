import requests
from datetime import datetime
import ssl

# SSL sertifika doğrulamasını devre dışı bırakmak için
ssl._create_default_https_context = ssl._create_unverified_context


# Firebase yapılandırma bilgilerini burada girin
config = {
    "apiKey": "apiii",
    "authDomain": "ekmek-sayaci.firebaseapp.com",
    "databaseURL": "https://ekmek-sayaci-default-rtdb.firebaseio.com/",
    "projectId": "ekmek-sayaci",
    "storageBucket": "ekmek-sayaci.appspot.com",
    "messagingSenderId": "762075188413",
    "appId": "1:762075188413:android:6b783fdffdac4031557bd4"
}

BASE_URL = config['databaseURL']

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
        response = requests.post(f"{BASE_URL}/islemler.json", json=islem_verisi)
        response.raise_for_status()
        print("İşlem başarıyla kaydedildi:", islem_verisi)
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Tüm işlemleri çekme fonksiyonu
def tum_islemleri_getir():
    try:
        response = requests.get(f"{BASE_URL}/islemler.json")
        response.raise_for_status()
        islemler = response.json()
        return islemler
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []

def add_user(user_data):
    try:
        # Kullanıcı verisini Firebase'e ekle
        response = requests.post(f"{BASE_URL}/users.json", json=user_data)
        response.raise_for_status()
        user_id = response.json()['name']  # Firebase, eklenen verinin anahtarını döner
        print("Kullanıcı başarıyla eklendi:", user_id, user_data)
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Çözümleme Hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def tum_kullanicilari_getir():
    try:
        response = requests.get(f"{BASE_URL}/users.json")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return {}

def kullanici_ekle(isim, sifre):
    user_data = {
        "name": isim,
        "password": sifre
    }
    # Kullanıcıyı ekle
    add_user(user_data)

def dogrulama(isim, sifre):
    global dogrumu
    try:
        users = tum_kullanicilari_getir()  # Kullanıcı verilerini al
        if not users:  # Eğer kullanıcı yoksa
            dogrumu = False
            return False
    

        for user_id, user_data in users.items():
            if user_data and user_data.get('name') == isim:
                if user_data.get('password') == sifre:
                    dogrumu = True
                    return True  # Doğru giriş
                    
        dogrumu = False
        return False  # Hatalı giriş
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        dogrumu = False
        return False

# Sayaç oluşturma
def initialize_counter():
    try:
        # "sayaç" adında bir düğüm oluştur ve değerini 0 olarak ayarla
        response = requests.put(f"{BASE_URL}/sayaç.json", json=0)
        response.raise_for_status()
        print("Sayaç başarıyla oluşturuldu.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Sayaç değerini al
def get_counter_value():
    try:
        response = requests.get(f"{BASE_URL}/sayaç.json")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None

# Sayaçta toplama işlemi yap
def increment_counter(amount):
    try:
        current_value = get_counter_value()
        if current_value is not None:
            new_value = current_value + amount
            requests.put(f"{BASE_URL}/sayaç.json", json=new_value)
            print(f"Sayaç güncellendi: {new_value}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Sayaçta çıkarma işlemi yap
def decrement_counter(amount):
    try:
        current_value = get_counter_value()
        if current_value is not None:
            new_value = current_value - amount
            requests.put(f"{BASE_URL}/sayaç.json", json=new_value)
            print(f"Sayaç güncellendi: {new_value}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
