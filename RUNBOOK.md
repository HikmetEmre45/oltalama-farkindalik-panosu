# Olay Müdahale Planı (Incident Response Runbook)
**Senaryo:** Tehdit Verisi API / Bulut Gizli Anahtarı Sızıntısı  
**Sorumlu:** Hikmet Emre Gültekin (2516016024) - Büyük Veri Analistliği  
**Kapsam:** Veri İhlali ve Oltalama Farkındalık Panosu & Bulut Fonksiyonları  

---

### 1. Aşama: Tespit (Detection)
* **Otomatik Uyarı:** GitHub Secret Scanning veya Gitleaks botu tarafından repoya anahtar itildiği tespit edildiğinde güvenlik e-postası tetiklenir.
* **Anomali Tespiti:** Bulut izleme panelinde (Azure / Cloudflare) beklenmeyen istek trafiği veya maliyet alarmı (%80 eşik aşımı) kontrol edilir.
* **İlk İşlem:** Sızıntının gerçekleştiği commit SHA değeri, sızan anahtarın adı ve yetki kapsamı derhal not edilir.

---

### 2. Aşama: İptal (Revocation & Invalidation)
* **Erişimi Kes:** İlgili veri sağlayıcının geliştirici konsoluna (URLhaus / OpenPhish / Bulut Sağlayıcı) girilir.
* **Anahtarı Geçersiz Kıl:** Sızan API token derhal "Revoke / Delete" seçeneğiyle iptal edilir; yetkisiz dış çağrılar engellenir.
* **Geçici İzolasyon:** Gerekirse serverless fonksiyonun dış ağ erişimi geçici olarak durdurulur (Down-time).

---

### 3. Aşama: Yenileme ve Güvenli Dağıtım (Key Rotation & Deployment)
* **Yeni Anahtar Üretimi:** Sağlayıcı panelinden en az yetki ilkesine (Least Privilege) uygun, salt-okunur yeni bir API anahtarı üretilir.
* **Kasaya Tanımlama:** Yeni anahtar kesinlikle koda veya depoya yazılmaz; doğrudan GitHub Secrets (`PROD_API_KEY`) veya Cloud Vault ortam değişkenlerine eklenir.
* **Yeniden Yayına Alma:** CI/CD hattı tetiklenerek uygulamanın yeni gizli anahtarla çalışması sağlanır.

---

### 4. Aşama: İnceleme ve Adli Bilişim (Investigation & Audit)
* **Erişim Logları:** Sızıntı anı ile iptal anı arasındaki uç nokta erişim logları incelenir; anormal IP'lerden gelen istekler filtrelenir.
* **Veri İhlali Kontrolü:** Fonksiyon üzerinden yetkisiz veri çekilip çekilmediği veya kaynak tüketimi yapılıp yapılmadığı doğrulanır.
* **Geçmişi Temizleme:** Sızan commit `git filter-repo` veya `BFG Repo-Cleaner` ile yerel ve uzak git geçmişinden kalıcı olarak kazınır.

---

### 5. Aşama: Bildirim ve Raporlama (Notification & Post-Mortem)
* **Ders Sorumlusu Bildirimi:** Durum ve alınan önlemler ders öğretim elemanına bildirilir.
* **Kök Neden Analizi:** Sızıntıya yol açan eksik `.gitignore` kuralı veya eksik branch protection kuralı raporlanır.
* **Kapatma:** Olay raporu tamamlanarak güvenlik takip kaydı kapatılır.