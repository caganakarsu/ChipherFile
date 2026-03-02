import os
from cryptography.fernet import Fernet

ANAHTAR_DOSYASI = "gizli.key"

def anahtar_uret_ve_kaydet():
    # Eğer sistemde daha önce üretilmiş bir anahtar yoksa, 
    # rastgele yeni bir AES anahtarı üretir ve 'gizli.key' adıyla kaydeder.
    
    if not os.path.exists(ANAHTAR_DOSYASI):
        anahtar = Fernet.generate_key()
        with open(ANAHTAR_DOSYASI, "wb") as dosya:
            dosya.write(anahtar)
        print("Sistem: Yeni bir şifreleme anahtarı başarıyla oluşturuldu!")

def anahtar_yukle():
    # Diske kaydedilmiş olan 'gizli.key' dosyasını okur ve anahtarı döndürür.
    if not os.path.exists(ANAHTAR_DOSYASI):
        raise FileNotFoundError("Kritik Hata: Şifreleme anahtarı (gizli.key) bulunamadı!")
    
    with open(ANAHTAR_DOSYASI, "rb") as dosya:
        return dosya.read()

def veriyi_sifrele(saf_veri):
    # Saf byte verisini alır, sistemdeki anahtarla kilitler 
    # ve şifrelenmiş byte verisini geri döndürür.
    

    anahtar = anahtar_yukle()
    f = Fernet(anahtar) # Şifreleme makinesini anahtarla çalıştırır.
    sifreli_veri = f.encrypt(saf_veri)
    return sifreli_veri

def veriyi_coz(sifreli_veri):
    # Şifreli byte verisini alır, sistemdeki doğru anahtarla kilidini açar
    # ve orijinal saf veriyi geri döndürür.
    
    
    anahtar = anahtar_yukle()
    f = Fernet(anahtar)
    
    try:
        orijinal_veri = f.decrypt(sifreli_veri)
        return orijinal_veri
    except Exception as e:
        # Eğer yanlış dosya veya yanlış anahtar denenirse programın çökmemesi için.
        raise ValueError("Şifre çözülemedi! Anahtar yanlış veya dosya bozuk.")