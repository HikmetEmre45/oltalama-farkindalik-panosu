# Veri İhlali ve Oltalama Farkındalık Panosu
**Ders:** Bulut Bilişim ve Siber Güvenlik · Güvenli Bulut Yayını  
**Öğrenci:** Hikmet Emre Gültekin (2516016024)  
**Öğretim Elemanı:** Öğr. Gör. Osman Can Çetlenbik  

---

### 📌 CV Başarı Cümlesi
> "Oltalama tehdit istihbaratı verilerini işleyen sunucusuz web panosunu 0 TL bütçe hedefiyle bulutta yayına aldım; istemci tarafında zararlı link yürütülmesini engelleyen güvenli mimari, girdi boyutu sınırlı regex defang motoru ve 10 birim test vakası ile uçtan uca uygulama güvenliğini sağladım."

---

### 🚀 Canlı Sistem ve Bağlantılar
* **Canlı Pano:** [Veri İhlali ve Oltalama Farkındalık Panosu](https://hikmetemre45.github.io/oltalama-farkindalik-panosu/)
* **Güvenlik Politikası:** [/.well-known/security.txt](https://hikmetemre45.github.io/oltalama-farkindalik-panosu/.well-known/security.txt)

---

### 🛡️ Mimari ve Güvenlik Sınırları (Trust Boundary)
1. **İstemci İzolasyonu:** Pano üzerindeki hiçbir tehdit URL'si HTML `<a>` etiketi olarak işlenmez; tüm veriler salt metin (plaintext) olarak render edilir.
2. **Sunucu Taraflı Defang Motoru:** `serverless_defang.py` modülü ile maksimum 2048 karakter girdi sınırı uygulanır; protokoller ve alan adı ayıraçları etkisizleştirilir (`hxxp://`, `[.]`, `[@]`).
3. **Doğrulama Testleri:** 10 farklı saldırı ve uç senaryoyu kapsayan birim testleri (unit tests) başarıyla geçmiştir.
4. **Altyapı (IaC):** `main.tf` Terraform dosyası ile kaynak grubu, statik hosting ve maliyet alarmı kod olarak tanımlanmıştır.
5. **Olay Müdahale:** API anahtarı sızıntı senaryosuna karşı 5 aşamalı `RUNBOOK.md` planı hazırdır.

---

### 🤖 Yapay Zekâ Beyanı
Uygulama kodlarının sertleştirilmesi, Terraform altyapı şablonu ve regex defang kurallarının birim test senaryolarında yapay zekâ araçlarından destek alınmıştır. Yapılandırmalar yerel ortamda test edilmiş ve doğrulanmıştır.
