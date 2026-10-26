import unittest
import re

# --- 1. ZORUNLU GÜVENLİK KONTROLÜ: GİRDİ BOYUTU VE DEFANG MOTORU ---
MAX_URL_LENGTH = 2048  # Girdi boyut sınırı (Buffer/DDoS koruması)

def defang_url(raw_url: str) -> str:
    """
    Zararlı URL'lerin tarayıcıda tıklanabilir linke dönüşmesini engellemek için
    protokol ve alan adı ayıraçlarını güvenli metne dönüştürür.
    """
    if not isinstance(raw_url, str):
        raise ValueError("Geçersiz veri tipi.")
    
    # Girdi boyut kontrolü
    if len(raw_url) > MAX_URL_LENGTH:
        raise ValueError("Girdi boyut sınırı aşıldı (Max 2048 karakter).")
    
    cleaned = raw_url.strip()
    
    # Protokolleri etkisizleştir (http -> hxxp, https -> hxxps)
    cleaned = re.sub(r'^http://', 'hxxp://', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'^https://', 'hxxps://', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'^ftp://', 'fxp://', cleaned, flags=re.IGNORECASE)
    
    # Noktaları ve ayracı etkisizleştir (. -> [.], @ -> [@])
    cleaned = cleaned.replace('.', '[.]')
    cleaned = cleaned.replace('@', '[@]')
    
    return cleaned


# --- 2. ZORUNLU DOĞRULAMA TESTİ: 10 BİRİM TEST VAKASI (UNIT TESTS) ---
class TestUrlDefang(unittest.TestCase):
    def test_01_http_standard(self):
        self.assertEqual(defang_url("http://malicious-site.com"), "hxxp://malicious-site[.]com")

    def test_02_https_standard(self):
        self.assertEqual(defang_url("https://phishing-bank.net/login"), "hxxps://phishing-bank[.]net/login")

    def test_03_ip_address(self):
        self.assertEqual(defang_url("http://192.168.1.1/payload.exe"), "hxxp://192[.]168[.]1[.]1/payload[.]exe")

    def test_04_subdomains(self):
        self.assertEqual(defang_url("https://secure.login.verify.update.com"), "hxxps://secure[.]login[.]verify[.]update[.]com")

    def test_05_credential_leak(self):
        self.assertEqual(defang_url("http://admin:1234@badsite.org"), "hxxp://admin:1234[@]badsite[.]org")

    def test_06_ftp_protocol(self):
        self.assertEqual(defang_url("ftp://drop-server.ru/file"), "fxp://drop-server[.]ru/file")

    def test_07_case_insensitivity(self):
        self.assertEqual(defang_url("HTTP://SCAM-PORTAL.COM"), "hxxp://SCAM-PORTAL[.]COM")

    def test_08_long_query_params(self):
        url = "https://phish.com/index.php?token=xyz123&redirect=account.php"
        expected = "hxxps://phish[.]com/index[.]php?token=xyz123&redirect=account[.]php"
        self.assertEqual(defang_url(url), expected)

    def test_09_input_size_limit(self):
        oversized_url = "http://bad.com/" + ("A" * 2050)
        with self.assertRaises(ValueError):
            defang_url(oversized_url)

    def test_10_invalid_type_protection(self):
        with self.assertRaises(ValueError):
            defang_url(123456)


if __name__ == '__main__':
    print("=" * 55)
    print("[-] Defang Birim Testleri Çalıştırılıyor (10 Vaka)...")
    print("=" * 55)
    unittest.main()