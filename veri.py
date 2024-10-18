import requests
from datetime import datetime

# Firebase yapılandırma bilgileri
config = {
    "databaseURL": "https://ekmek-sayaci-default-rtdb.firebaseio.com/"
}

dogrumu = None

# İşlem kaydetme fonksiyonu
def islem_kaydet(kullanici, islem_turu, miktar):
    try:
        islem_verisi = {
            "kullanici": kullanici,
            "islem_turu": islem_turu,
            "miktari": miktar,
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        url = f"{config['databaseURL']}islemler.json"  # .json uzantısı kullan
        response = requests.post(url, json=islem_verisi)  # Veriyi JSON olarak POST isteği ile gönder
        if response.status_code == 200:
            print("İşlem başarıyla kaydedildi:", islem_verisi)
        else:
            print(f"İşlem kaydedilemedi, hata: {response.status_code}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Tüm işlemleri al
def tum_islemleri_getir():
    try:
        url = f"{config['databaseURL']}islemler.json"  # .json uzantısı ile URL
        response = requests.get(url)  # GET isteği ile işlemleri al
        if response.status_code == 200:
            islemler = response.json()
            return islemler if islemler else {}
        else:
            print(f"İşlemler alınamadı, hata: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return {}

# Yeni kullanıcı ekleme fonksiyonu
def add_user(user_id, user_data):
    try:
        url = f"{config['databaseURL']}users/{user_id}.json"  # Kullanıcı ID'si ile .json uzantılı URL
        response = requests.put(url, json=user_data)  # Veriyi JSON formatında PUT isteği ile gönder
        if response.status_code == 200:
            print("Kullanıcı başarıyla eklendi:", user_data)
        else:
            print(f"Kullanıcı eklenemedi, hata: {response.status_code}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Kullanıcı ID oluşturma fonksiyonu
def generate_user_id():
    try:
        url = f"{config['databaseURL']}users.json"
        response = requests.get(url)
        if response.status_code == 200:
            users = response.json()
            if isinstance(users, dict):  # Kullanıcı verisi sözlükse
                return str(len(users) + 1)  # Mevcut kullanıcı sayısına 1 ekleyin
            return "1"  # Eğer hiç kullanıcı yoksa ID'yi "1" olarak belirleyin
        else:
            print(f"Kullanıcı ID'si oluşturulamadı, hata: {response.status_code}")
            return None
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None

# Kullanıcı ekleme
def kullanici_ekle(isim, sifre):
    user_id = generate_user_id()  # Yeni kullanıcı ID'sini oluştur
    if user_id:
        user_data = {
            "name": isim,
            "password": sifre
        }
        add_user(user_id, user_data)

# Kullanıcı doğrulama
def dogrulama(isim, sifre):
    global dogrumu
    try:
        url = f"{config['databaseURL']}users.json"
        response = requests.get(url)
        if response.status_code == 200:
            users = response.json()
            if not users:
                dogrumu = False
                return False

            if isinstance(users, dict):  # Kullanıcı verisi sözlükse
                for user_id, user_data in users.items():
                    if user_data.get('name') == isim and user_data.get('password') == sifre:
                        dogrumu = True  # Doğru giriş
                        return True
            else:  # Eğer liste ise
                for user_data in users:
                    if user_data.get('name') == isim and user_data.get('password') == sifre:
                        dogrumu = True  # Doğru giriş
                        return True

            dogrumu = False
            return False
        else:
            print(f"Kullanıcı doğrulaması yapılamadı, hata: {response.status_code}")
            return False
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return False

# Sayaç oluşturma
def initialize_counter():
    try:
        url = f"{config['databaseURL']}sayaç.json"
        response = requests.put(url, json=0)  # Sayaç değerini 0 olarak başlat
        if response.status_code == 200:
            print("Sayaç başarıyla oluşturuldu.")
        else:
            print(f"Sayaç oluşturulamadı, hata: {response.status_code}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Sayaç değerini alma
def get_counter_value():
    try:
        url = f"{config['databaseURL']}sayaç.json"
        response = requests.get(url)  # GET isteği ile sayaç değerini al
        if response.status_code == 200:
            return response.json()  # Sayaç değerini döndür
        else:
            print(f"Sayaç alınamadı, hata: {response.status_code}")
            return None
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None

# Sayaçta toplama işlemi yap
def increment_counter(amount):
    try:
        current_value = get_counter_value()
        if current_value is not None:
            new_value = current_value + amount
            url = f"{config['databaseURL']}sayaç.json"
            response = requests.put(url, json=new_value)  # Sayaç değerini güncelle
            if response.status_code == 200:
                print(f"Sayaç güncellendi: {new_value}")
            else:
                print(f"Sayaç güncellenemedi, hata: {response.status_code}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Sayaçta çıkarma işlemi yap
def decrement_counter(amount):
    try:
        current_value = get_counter_value()
        if current_value is not None:
            new_value = current_value - amount
            url = f"{config['databaseURL']}sayaç.json"
            response = requests.put(url, json=new_value)  # Sayaç değerini güncelle
            if response.status_code == 200:
                print(f"Sayaç güncellendi: {new_value}")
            else:
                print(f"Sayaç güncellenemedi, hata: {response.status_code}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
