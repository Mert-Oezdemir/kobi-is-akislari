# KOBİ İş Akışları — Açık Kaynak Başlangıç Kiti

**Türkçe · Bağımsız topluluk projesi · Apache-2.0**

Küçük işletmelerde tekrarlanan işleri **insan onayını koruyarak** hazırlamak için örnek Claude becerileri (skills) ve çevrimdışı çalışan Python araçları. Gerçek hesaplara bağlantı kurmadan da sentetik CSV verileriyle deneyebilirsiniz.

> **Bağımsız proje:** Anthropic tarafından hazırlanmış, desteklenmiş veya onaylanmış değildir. "Claude" ve "Cowork" adları yalnızca uyumluluğu tarif etmek için geçer. Anthropic'in resmî **Small Business** eklentisi farklı bir üründür: https://github.com/anthropics/knowledge-work-plugins/tree/main/small-business

## İçindekiler

| Modül | Ne sağlar? | Sınır |
| --- | --- | --- |
| `kobi-fatura` | Gecikmiş faturaları sınıflandırır; hatırlatma taslakları | E-posta **göndermez** |
| `kobi-crm` | Mükerrer kişiler, eksik alanlar, durgun fırsatlar | CRM'de kayıt **değiştirmez** |
| `kobi-sozlesme` | Taslak sözleşme kontrol listesi ve risk soruları | Hukuki mütalaa **değildir** |
| `kobi-sikayet` | Şikâyet için empatik cevap taslağı | Müşteriye **göndermez** |
| `kobi-baslangic` | Yetki, veri ve iş akışı kontrolüyle ilk kurulum | Otomatik bağlantı **kurmaz** |
| `python -m kobi_akis` | CSV ve düz metinden denetlenebilir raporlar | Yalnızca **yerel dosyalar** |

## Hızlı deneme — herhangi bir Claude hesabı olmadan

Python 3.10 veya üzeri yeterlidir; ek paket kurulumu gerekmez.

```bash
python -m kobi_akis invoices --input examples/invoices.csv --today 2026-10-14 --output out/faturalar.md
python -m kobi_akis crm --contacts examples/contacts.csv --deals examples/deals.csv --today 2026-10-14 --output out/crm.md
python -m kobi_akis contract --input examples/sample-contract.txt --output out/sozlesme.md
python -m unittest discover -s tests -v
```

Komutlar yalnızca rapor üretir; e-posta, ödeme veya CRM güncellemesi yapmaz. `out/` klasörü Git tarafından yok sayılır. Örneklerdeki kişi/kurum adları ve e-posta adresleri hayalidir.

## Claude Cowork'te becerileri kullanma

1. [Claude Desktop](https://claude.ai/download) uygulamasını açın; hesabınızdaki Cowork ve eklenti erişimini kontrol edin.
2. Cowork içinde **Customize → Plugins** bölümüne gidin. Uygulamanızın desteklediği yöntemle bu klasörü yerel özel eklenti olarak yükleyin (arayüz ve plan koşulları değişebilir).
3. `/kobi-baslangic` ile başlayın. Sadece ihtiyaç duyduğunuz veriyi paylaşın; gerçek erişim izinlerini kendiniz verin.
4. `/kobi-fatura`, `/kobi-crm`, `/kobi-sozlesme` veya `/kobi-sikayet` becerilerini çalıştırın. Herhangi bir dış sisteme yazma/gönderme öncesinde sonucu inceleyin.

Bu depo **resmî QuickBooks, PayPal, HubSpot, Gmail veya DocuSign bağlantılarını paketlemez**; varsa, bağlı araçlarınızın kendi yetki modelini ve resmî kullanım şartlarını izlemelisiniz. Canlı entegrasyonlar ayrıca geliştirilip test edilmelidir. Beceri yönergeleri işlem onayını şart koşar; bunun teknik olarak her entegrasyonda otomatik garanti edildiği iddia edilmez.

## Örnek verinin biçimi

- `invoices.csv`: `invoice_id,customer,email,amount,currency,due_date,status`; `due_date` ISO `YYYY-MM-DD`; durumlar `paid`, `cancelled` veya `open` olabilir.
- `contacts.csv`: `contact_id,name,email,phone`; tekrarlar yalnızca birebir normalize edilmiş e-posta eşleşmesine göre önerilir.
- `deals.csv`: `deal_id,name,stage,owner,last_activity_date`; açık fırsatlarda **30 günü aşan** hareketsizlik raporlanır.
- `sample-contract.txt`: `.txt` / `.md` dokümanlar için basit anahtar sözcük taraması; hukuki karar vermez.

Para birimleri raporda özgün haliyle tutulur; farklı para birimleri toplamı birleştirilmez. Fatura tutarları finansal doğruluk için Python `Decimal` kullanılarak işlenir. Hatalı ya da eksik kayıtlar sessizce tahmin edilmez, hata olarak gösterilir.

## Güvenlik, izinler ve lisans

- Yerel betikler ağ bağlantısı kullanmaz; hiçbir veri uzaktaki servise aktarılmaz.
- `.gitignore`, `.env`, yerel raporlar ve özel veri klasörlerini dışarıda tutar. Yine de **push öncesi dosyaları kontrol edin**.
- Finans, vergi, İK ve sözleşme kararlarını ilgili uzmanınıza teyit ettirin.
- Kod ve özgün belgeler [Apache License 2.0](LICENSE) altındadır; değişiklik yapıp dağıtırken lisans ve telif bildirimlerini koruyun.
- Anthropic/Claude, QuickBooks, PayPal, HubSpot, DocuSign, Gmail ve Canva üçüncü taraf ticari markalardır. İlgili firmalar bu projeyi desteklememektedir.
- Üçüncü taraf metin, görsel, logo, resmi eklenti kodu veya çevrilmiş rehber **bu depoya kopyalanmamıştır**. Kaynak/atıf yaklaşımı için [CREDITS.md](CREDITS.md) dosyasına bakın.

## Önerilen ilk iş akışı

Sentetik `invoices.csv` dosyasını işleyin; raporda hangi faturanın neden geciktiğini inceleyin. Hatırlatma metinlerini ayrıca düzeltin. Ancak doğru müşteri, doğru tutar, uygun dil ve gönderim zamanı kontrol edildikten sonra, **kendi e-posta aracınızda manuel** gönderin.

Katkı: Testi geçen küçük PR'lar tercih edilir. Güvenlik açığı paylaşımı için [SECURITY.md](SECURITY.md).
