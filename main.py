import customtkinter as ctk
from tkinter import filedialog, messagebox
import file_operations
import cipher_engine


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CipherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Program açılır açılmaz şifreleme anahtarını hazırlar.
        # Eğer klasörde gizli.key yoksa hemen yenisini üretir.
        cipher_engine.anahtar_uret_ve_kaydet()

        self.title("CipherFile - Güvenli Dosya")
        self.geometry("500x400")
        self.resizable(False, False)

        self.secilen_dosya = None

        self.baslik = ctk.CTkLabel(self, text="Dosya Şifreleme Sistemi", font=("Arial", 24, "bold"))
        self.baslik.pack(pady=30)

        self.btn_dosya_sec = ctk.CTkButton(self, text="📁 Dosya Seç", command=self.dosya_sec)
        self.btn_dosya_sec.pack(pady=10)

        self.lbl_dosya_yolu = ctk.CTkLabel(self, text="Henüz bir dosya seçilmedi.", text_color="gray")
        self.lbl_dosya_yolu.pack(pady=10)

        self.btn_sifrele = ctk.CTkButton(self, text="🔒 Şifrele", fg_color="#28a745", hover_color="#218838", command=self.sifrele)
        self.btn_sifrele.pack(pady=15)

        self.btn_coz = ctk.CTkButton(self, text="🔓 Şifre Çöz", fg_color="#dc3545", hover_color="#c82333", command=self.sifre_coz)
        self.btn_coz.pack(pady=5)

    def dosya_sec(self):
        dosya_yolu = filedialog.askopenfilename(title="İşlem yapılacak dosyayı seçin")
        if dosya_yolu:
            self.secilen_dosya = dosya_yolu
            self.lbl_dosya_yolu.configure(text=f"Seçilen: {dosya_yolu}", text_color="white")

    def sifrele(self):
        if not self.secilen_dosya:
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin!")
            return
        
        try:
            # 1) Dosyayı file_operations ile okur.
            saf_veri = file_operations.dosya_oku(self.secilen_dosya)
            
            # 2) Veriyi cipher_engine ile şifreler.
            sifreli_veri = cipher_engine.veriyi_sifrele(saf_veri)
            
            # 3) Yeni dosyayı file_operations ile kaydeder.
            yeni_dosya_yolu = self.secilen_dosya + ".sifreli"
            file_operations.dosya_yaz(yeni_dosya_yolu, sifreli_veri)
            
            messagebox.showinfo("Başarılı", f"Dosya başarıyla şifrelendi!\n\nOluşturulan Dosya: {yeni_dosya_yolu}")
        except Exception as e:
            messagebox.showerror("Hata", f"Şifreleme sırasında bir hata oluştu:\n{e}")

    def sifre_coz(self):
        if not self.secilen_dosya:
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin!")
            return
        
        try:
            # 1) Şifreli dosyayı okur.
            sifreli_veri = file_operations.dosya_oku(self.secilen_dosya)
            
            # 2) Şifreyi çözer.
            cozulmus_veri = cipher_engine.veriyi_coz(sifreli_veri)
            
            # 3) Çözülmüş halini yeni isimle kaydeder.
            if self.secilen_dosya.endswith(".sifreli"):
                yeni_dosya_yolu = self.secilen_dosya.replace(".sifreli", "_cozuldu.txt")
            else:
                yeni_dosya_yolu = self.secilen_dosya + "_cozuldu"
                
            file_operations.dosya_yaz(yeni_dosya_yolu, cozulmus_veri)
            
            messagebox.showinfo("Başarılı", f"Şifre başarıyla çözüldü!\n\nOluşturulan Dosya: {yeni_dosya_yolu}")
        except Exception as e:
            messagebox.showerror("Hata", "Şifre çözülemedi!\nBüyük ihtimalle gizli.key dosyası değişti veya seçilen dosya bozuk.")

if __name__ == "__main__":
    app = CipherApp()
    app.mainloop()