---
name: kobi-fatura
description: Ödenmemiş faturaları tespit etme, vadesi geçenleri sınıflandırma, insan denetimi için ödeme hatırlatma taslağı hazırlama. "Fatura takibi" veya "kim borçlu" isteklerinde kullan.
---

# Fatura takibi: önce rapor, sonra onay

- Veri kaynağı: kullanıcının onayladığı, erişilebilir muhasebe bağlantısı veya `invoice_id,customer,email,amount,currency,due_date,status` sütunlu CSV. Bağlantı yoksa bir bağlantı varmış gibi davranma.
- Ödenmiş/iptal kayıtları dışarıda bırak. Son ödeme tarihi geçmiş açık faturaları hesapla; bugünün tarihini açık belirt. Tutarları para birimine göre ayrı göster.
- Eksik tutar, para birimi, durum veya tarih gördüğünde kaydı "doğrulama gerekli" olarak işaretle; para veya ödeme tarihi uydurma.
- Her müşteri için saygılı bir **taslak** yaz; alıcı adresini, referans numarasını, gecikme gününü ve tutarı göster. Önce ilişki tonunun uygunluğunu sor.
- **Kritik onay:** Hiçbir e-posta gönderme, otomatik ödeme isteği yaratma veya muhasebe kaydı değiştirme. Bunlar için kullanıcıdan ayrı ayrı, açık onay gerekir.
- CLI örneği: `python -m kobi_akis invoices --input examples/invoices.csv --today 2026-10-14 --output out/faturalar.md`.

Finansal karar için rapor muhasebeci veya sorumlu kişi tarafından kontrol edilmelidir.
