import os


def dosya_oku(dosya_yolu):
    # Dosyayı binary formatta okur ve içindeki saf veriyi döndürür.
    if not os.path.exists(dosya_yolu):
        raise FileNotFoundError(f"Hata: İşlem yapılmak istenen dosya bulunamadı -> {dosya_yolu}")
    
    with open(dosya_yolu, "rb") as dosya:
        return dosya.read()

def dosya_yaz(dosya_yolu, veri):
    # Şifrelenmiş veya çözülmüş veriyi, belirtilen yola binary formatta yazar.
    with open(dosya_yolu, "wb") as dosya:
        dosya.write(veri)