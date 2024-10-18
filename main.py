from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock  # Zamanlayıcı için Clock sınıfını ekleyin
import os
import veri

class GirisEkrani(BoxLayout):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.sm = sm  # ScreenManager referansı

        # Resim ekleme 
        self.logo = Image(source='assets/images/ekmek.png', size_hint=(1, 0.5))  # image kaynağı ekleniyor
        self.add_widget(self.logo)

        # Kullanıcı adı etiketi ve giriş alanı
        self.label1 = Label(text="Kullanıcı Adınızı Giriniz.", font_size='18sp', size_hint=(1, 0.1))
        self.add_widget(self.label1)

        self.entry1 = TextInput(hint_text="Kullanıcı Adı", multiline=False, font_size='16sp')
        self.add_widget(self.entry1)

        # Şifre etiketi ve giriş alanı
        self.label2 = Label(text="Şifrenizi Giriniz.", font_size='18sp', size_hint=(1, 0.1))
        self.add_widget(self.label2)

        self.entry2 = TextInput(hint_text="Şifre", password=True, multiline=False, font_size='16sp')
        self.add_widget(self.entry2)

        # Düğme düzeni
        button_layout = GridLayout(cols=2, size_hint=(1, 0.2))

        # Giriş düğmesi
        self.button1 = Button(text="Giriş", font_size='18sp')
        self.button1.bind(on_press=self.giris_butonuna_basilinca)
        button_layout.add_widget(self.button1)

        # Kayıt Ol düğmesi
        self.button2 = Button(text="Kayıt Ol", font_size='16sp')
        self.button2.bind(on_press=self.kayit_ol_butonuna_basilinca)
        button_layout.add_widget(self.button2)

        # Düğmeleri ekle
        self.add_widget(button_layout)

    def giris_butonuna_basilinca(self, instance):
        kullanici_adi = self.entry1.text.strip()
        sifre = self.entry2.text.strip()

        veri.dogrulama(kullanici_adi, sifre)
        if veri.dogrumu == True:
            self.show_message("Giriş yapılıyor.")
            # Giriş bilgilerini bir dosyaya kaydet
            with open("giris_durumu.txt", "w") as file:
                file.write(f"KullaniciAdi:{kullanici_adi}")
            self.sm.current = 'ana'
        else:
            self.show_message("Kullanıcı adı veya şifre hatalı !")

    def kayit_ol_butonuna_basilinca(self, instance):
        # Kayıt ekranına geçiş yap
        self.sm.current = 'kayit'

    def show_message(self, message):
        # Mesajın gösterileceği içerik için bir BoxLayout oluştur
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Mesajı gösteren label
        message_label = Label(text=message, size_hint_y=None, height=100)
        layout.add_widget(message_label)

        # Kapatma butonu
        close_button = Button(text='Kapat', size_hint_y=None, height=40)
        close_button.bind(on_release=lambda x: popup.dismiss())  # Butona tıklandığında pop-up'ı kapat

        # Butonu layout'a ekle
        layout.add_widget(close_button)

        # Pop-up mesajı oluştur
        popup = Popup(title='Mesaj',
                      content=layout,
                      size_hint=(None, None),  # Boyut ayarları
                      size=(400, 200))  # İstediğiniz boyutları ayarlayın

        # Pop-up'ı göster
        popup.open()

class KayitEkrani(BoxLayout):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.sm = sm  # ScreenManager referansı

        # Kullanıcı adı etiketi ve giriş alanı
        self.label1 = Label(text="Kullanıcı Adı Belirleyin", font_size='18sp', size_hint=(1, 0.1))
        self.add_widget(self.label1)

        self.entry1 = TextInput(hint_text="Kullanıcı Adı", multiline=False, font_size='16sp')
        self.add_widget(self.entry1)

        # Şifre etiketi ve giriş alanı
        self.label2 = Label(text="Şifrenizi Belirleyin", font_size='18sp', size_hint=(1, 0.1))
        self.add_widget(self.label2)

        self.entry2 = TextInput(hint_text="Şifre", password=True, multiline=False, font_size='16sp')
        self.add_widget(self.entry2)

        # Şifre tekrarı etiketi ve giriş alanı
        self.label3 = Label(text="Şifrenizi Tekrar Girin", font_size='18sp', size_hint=(1, 0.1))
        self.add_widget(self.label3)

        self.entry3 = TextInput(hint_text="Şifre (Tekrar)", password=True, multiline=False, font_size='16sp')
        self.add_widget(self.entry3)

        # Kayıt ol düğmesi
        self.button1 = Button(text="Kayıt Ol", font_size='18sp')
        self.button1.bind(on_press=self.kayit_ol_butonuna_basilinca)
        self.add_widget(self.button1)

    def kayit_ol_butonuna_basilinca(self, instance):
        kullanici_adi = self.entry1.text.strip()
        sifre = self.entry2.text.strip()
        sifre_tekrar = self.entry3.text.strip()

        if not kullanici_adi or not sifre or not sifre_tekrar:
            self.show_message("Lütfen tüm alanları doldurun.")
            return

        if sifre != sifre_tekrar:
            self.show_message("Şifreler eşleşmiyor!")
            return

        if ':' in kullanici_adi:
            self.show_message("Kullanıcı adında ':' karakteri kullanılamaz.")
            return
                
        veri.kullanici_ekle(kullanici_adi, sifre)

        self.show_message("Kayıt başarılı! Giriş yapabilirsiniz.")
        self.sm.current = 'giris'


    def show_message(self, message):
        # Mesajın gösterileceği içerik için bir BoxLayout oluştur
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Mesajı gösteren label
        message_label = Label(text=message, size_hint_y=None, height=100)
        layout.add_widget(message_label)

        # Kapatma butonu
        close_button = Button(text='Kapat', size_hint_y=None, height=40)
        close_button.bind(on_release=lambda x: popup.dismiss())  # Butona tıklandığında pop-up'ı kapat

        # Butonu layout'a ekle
        layout.add_widget(close_button)

        # Pop-up mesajı oluştur
        popup = Popup(title='Mesaj',
                      content=layout,
                      size_hint=(None, None),  # Boyut ayarları
                      size=(400, 200))  # İstediğiniz boyutları ayarlayın

        # Pop-up'ı göster
        popup.open()

class AnaEkran(BoxLayout):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.sm = sm  # ScreenManager referansı

        # Resim ekleme
        self.logo = Image(source='assets/images/ekmek.png', size_hint=(1, 0.5))  # image kaynağı ekleniyor
        self.add_widget(self.logo)

        sayac = str(veri.get_counter_value())

        # SAYAC
        self.label2 = Label(text=sayac, font_size='18sp', size_hint=(1, 0.1))
        self.add_widget(self.label2)

        # Düğme düzeni
        button_layout = GridLayout(cols=2, size_hint=(1, 0.2))

        # ekmek ekle düğmesi
        self.button1 = Button(text="Ekmek ekle", font_size='18sp')
        self.button1.bind(on_press=self.ekmek_ekle)
        button_layout.add_widget(self.button1)

        # ekemek sil düğmesi
        self.button2 = Button(text="Ekmek Sil", font_size='16sp')
        self.button2.bind(on_press=self.ekmek_sil)
        button_layout.add_widget(self.button2)

        # KULLANICIDAN CIKIS düğmesi
        self.button4 = Button(text="Kullanıcıdan Çıkış", font_size='14sp')
        self.button4.bind(on_press=self.kullanicidan_cikis)
        button_layout.add_widget(self.button4)

        # LOG düğmesi
        self.button3 = Button(text="Tüm işlemler", font_size='14sp')
        self.button3.bind(on_press=self.tumislemler)
        button_layout.add_widget(self.button3)

        # Her saniye sayacı güncelle
        Clock.schedule_interval(self.sayac_guncelle, 3)

        # Düğmeleri ekle
        self.add_widget(button_layout)

    def kullanicidan_cikis(self, instance):
        # Çıkış yaparken giriş dosyasını sil
        if os.path.exists("giris_durumu.txt"):
            os.remove("giris_durumu.txt")
        self.sm.current = 'giris'

    def tumislemler(self, instance):
        # Tüm İşlemler ekranına geçiş yap
        self.sm.current = 'tum_islemler'

    def ekmek_ekle(self, instance):
        # ekmek ekleme ekranına geçiş yap
        self.sm.current = 'ekmek_ekleme'

    def ekmek_sil(self, instance):
        # ekmek silme ekranına geçiş yap
        self.sm.current = 'ekmek_silme'

    def sayac_guncelle(self, dt):
        # Veritabanından sayaç değerini al ve güncelle
        try:
            counter_value = veri.get_counter_value()  # Veritabanından sayaç değerini alın
            self.label2.text = str(counter_value)  # Label'ı güncelle
        except Exception as e:
            print(f"Hata oluştu: {e}")


class EkmekEklemeEkrani(BoxLayout):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.sm = sm  # ScreenManager referansı

        # Resim ekleme
        self.logo = Image(source='assets/images/ekmek.png', size_hint=(1, 0.5))  # image kaynağı ekleniyor
        self.add_widget(self.logo)

        # Düğme düzeni
        button_layout = GridLayout(cols=2, size_hint=(1, 0.2))

        # Eklenecek ekmek miktarı için widgetlar
        self.label1 = Label(text="Eklenecek Miktarı giriniz.", font_size='18sp', size_hint=(1, 0.1))
        self.add_widget(self.label1)

        self.entry1 = TextInput(hint_text="Miktar", multiline=False, font_size='16sp')
        self.add_widget(self.entry1)

        # Düğme düzeni
        button_layout = GridLayout(cols=2, size_hint=(1, 0.2))

        # ekle düğmesi
        self.button3 = Button(text="Ekle", font_size='16sp')
        self.button3.bind(on_press=self.ekle)

        # geri düğmesi
        self.button6 = Button(text="Geri", font_size='16sp')
        self.button6.bind(on_press=self.geri)

        # Düğmeleri ekle
        self.add_widget(button_layout)
        button_layout.add_widget(self.button3)
        button_layout.add_widget(self.button6)

    def ekle(self, instance):
        miktar = self.entry1.text.strip()

        try:
            miktar_int = int(miktar)  # Girişi tam sayıya dönüştürmeyi deniyoruz
            if miktar_int <= 0:
                self.show_message("Lütfen pozitif bir sayı giriniz.")
            else:
                veri.increment_counter(miktar_int)
                self.show_message(f"{miktar_int} tane ekmek eklendi.")
                
                # Giriş bilgileri var mı kontrol et
                if os.path.exists("giris_durumu.txt"):
                    with open("giris_durumu.txt", "r") as file:
                        kullanici_bilgisi = file.read()
                        kullanici = kullanici_bilgisi.replace("KullaniciAdi:", "")  # "kullaniciadi: " kısmını sil
                        veri.islem_kaydet(kullanici, "ekleme", miktar_int)

        except ValueError:
            # Eğer giriş sayı değilse bu blok çalışır
            self.show_message("Lütfen sadece sayı giriniz.")
        
    def geri(self, instance):
        # ana ekranına geçiş yap
        self.sm.current = 'ana'

    def show_message(self, message):
        # Mesajın gösterileceği içerik için bir BoxLayout oluştur
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Mesajı gösteren label
        message_label = Label(text=message, size_hint_y=None, height=100)
        layout.add_widget(message_label)

        # Kapatma butonu
        close_button = Button(text='Kapat', size_hint_y=None, height=40)
        close_button.bind(on_release=lambda x: popup.dismiss())  # Butona tıklandığında pop-up'ı kapat

        # Butonu layout'a ekle
        layout.add_widget(close_button)

        # Pop-up mesajı oluştur
        popup = Popup(title='Mesaj',
                      content=layout,
                      size_hint=(None, None),  # Boyut ayarları
                      size=(400, 200))  # İstediğiniz boyutları ayarlayın

        # Pop-up'ı göster
        popup.open()


class EkmekSilmeEkrani(BoxLayout):
    def __init__(self, sm, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.sm = sm  # ScreenManager referansı

        # Resim ekleme
        self.logo = Image(source='assets/images/ekmek.png', size_hint=(1, 0.5))  # image kaynağı ekleniyor
        self.add_widget(self.logo)

        # Düğme düzeni
        button_layout = GridLayout(cols=2, size_hint=(1, 0.2))

        # silincek ekmek miktarı için widgetlar
        self.label2 = Label(text="Silinecek Miktarı giriniz.", font_size='18sp', size_hint=(1, 0.1))
        self.add_widget(self.label2)

        self.entry2 = TextInput(hint_text="Miktar", multiline=False, font_size='16sp')
        self.add_widget(self.entry2)

        # Düğme düzeni
        button_layout = GridLayout(cols=2, size_hint=(1, 0.2))

        # sil düğmesi
        self.button4 = Button(text="Sil", font_size='16sp')
        self.button4.bind(on_press=self.sil)

        # geri düğmesi
        self.button5 = Button(text="Geri", font_size='16sp')
        self.button5.bind(on_press=self.geri)

        # Düğmeleri ekle
        self.add_widget(button_layout)
        button_layout.add_widget(self.button4)
        button_layout.add_widget(self.button5)

    def sil(self, instance):
        miktar = self.entry2.text.strip()
    
        try:
            miktar_int = int(miktar)  # Girişi tam sayıya dönüştürmeyi deniyoruz
            if miktar_int <= 0:
                self.show_message("Lütfen pozitif bir sayı giriniz.")
            else:
                veri.decrement_counter(miktar_int)
                self.show_message(f"{miktar_int} tane ekmek silindi.")

                # Giriş bilgileri var mı kontrol et
                if os.path.exists("giris_durumu.txt"):
                    with open("giris_durumu.txt", "r") as file:
                        kullanici_bilgisi = file.read()
                        kullanici = kullanici_bilgisi.replace("KullaniciAdi:", "")  # "kullaniciadi: " kısmını sil
                        veri.islem_kaydet(kullanici, "silme", miktar_int)

        except ValueError:
            # Eğer giriş sayı değilse bu blok çalışır
            self.show_message("Lütfen sadece sayı giriniz.")
    

    def geri(self, instance):
        # ana ekranına geçiş yap
        self.sm.current = 'ana'


    def show_message(self, message):
        # Mesajın gösterileceği içerik için bir BoxLayout oluştur
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Mesajı gösteren label
        message_label = Label(text=message, size_hint_y=None, height=100)
        layout.add_widget(message_label)

        # Kapatma butonu
        close_button = Button(text='Kapat', size_hint_y=None, height=40)
        close_button.bind(on_release=lambda x: popup.dismiss())  # Butona tıklandığında pop-up'ı kapat

        # Butonu layout'a ekle
        layout.add_widget(close_button)

        # Pop-up mesajı oluştur
        popup = Popup(title='Mesaj',
                      content=layout,
                      size_hint=(None, None),  # Boyut ayarları
                      size=(400, 200))  # İstediğiniz boyutları ayarlayın

        # Pop-up'ı göster
        popup.open()

class TumIslemlerEkrani(Screen):
    def __init__(self, sm, **kwargs):
        super(TumIslemlerEkrani, self).__init__(**kwargs)
        self.sm = sm
        self.orientation = 'vertical'  # Dikey düzen

        # ScrollView oluştur
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 1000))  # Boyutları ihtiyaca göre ayarlayın

        # BoxLayout oluştur
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Tüm işlemleri ekrana yazdırma kısmı
        islemler = veri.tum_islemleri_getir()
        for islem_id, islem_verisi in islemler.items():  # her islem için islem_id ve islem_verisi al
            label = Label(text=f"{islem_verisi['tarih']}: {islem_verisi['kullanici']} - {islem_verisi['islem_turu']} - {islem_verisi['miktari']}",
                          size_hint_y=None, height=40)
            layout.add_widget(label)

        # Layout'u ScrollView'a ekle
        scroll_view.add_widget(layout)

        # ScrollView'u ana layout'a ekle
        self.add_widget(scroll_view)

        # Geri düğmesi ekleyelim ve alta ortalayalım
        self.geri_button = Button(text="Geri", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        self.geri_button.bind(on_press=self.geri)
        self.add_widget(self.geri_button)

    def geri(self, instance):
        # Geri ana ekrana dönüş yapar
        self.sm.current = 'ana'


class GirisApp(App):
    def build(self):
        sm = ScreenManager()

        # Mevcut ekranları ekleyin
        giris_ekrani = Screen(name='giris')
        giris_ekrani.add_widget(GirisEkrani(sm))
        sm.add_widget(giris_ekrani)

        kayit_ekrani = Screen(name='kayit')
        kayit_ekrani.add_widget(KayitEkrani(sm))
        sm.add_widget(kayit_ekrani)

        ana_ekran = Screen(name='ana')
        ana_ekran.add_widget(AnaEkran(sm))
        sm.add_widget(ana_ekran)

        ekmek_ekleme_ekrani = Screen(name='ekmek_ekleme')
        ekmek_ekleme_ekrani.add_widget(EkmekEklemeEkrani(sm))
        sm.add_widget(ekmek_ekleme_ekrani)

        ekmek_silme_ekrani = Screen(name='ekmek_silme')
        ekmek_silme_ekrani.add_widget(EkmekSilmeEkrani(sm))
        sm.add_widget(ekmek_silme_ekrani)

        # Tüm İşlemler ekranı ekleniyor
        tum_islemler_ekrani = Screen(name='tum_islemler')
        tum_islemler_ekrani.add_widget(TumIslemlerEkrani(sm))
        sm.add_widget(tum_islemler_ekrani)

        # Giriş bilgileri var mı kontrol et
        if os.path.exists("giris_durumu.txt"):
            with open("giris_durumu.txt", "r") as file:
                kullanici_bilgisi = file.read()
                print(kullanici_bilgisi)
                if kullanici_bilgisi:
                    sm.current = 'ana'  # Eğer giriş bilgisi varsa direkt ana ekrana git
        else:
            sm.current = 'giris'  # İlk olarak giriş ekranı gösterilecek

        return sm


if __name__ == '__main__':
    GirisApp().run()
