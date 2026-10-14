---
name: kobi-crm
description: CRM'de aynı e-posta adresli kişiler, eksik kayıt alanları ve uzun süre güncellenmemiş fırsatlar için inceleme listesi oluşturma. "CRM temizliği" isteklerinde kullan.
---

# CRM kalite kontrolü

- Kaynak olarak sadece kullanıcı yetkiliyse bağlı CRM'yi veya açıkça paylaştığı CSV'leri kullan.
- Mükerrer kişi önerilerini yalnızca güçlü tanımlayıcıyla (ör. normalize edilmiş birebir e-posta) oluştur; aynı adlı kişileri otomatik birleştirme.
- Kişilerde eksik e-posta/ad alanlarını ve fırsatlarda eksik sorumluyu ayrı gruplar halinde çıkar.
- Durgun fırsatlar için son aktivite tarihine dayanan eşiği açıkla (varsayılan 30 gün); farklı ekiplerin aşama kuralları olabileceğini belirt.
- Birleştirme/silme/değiştirme yapma; her değişiklikten önce eski/yeni değerleri ve kayıt bağlantısını göster, eyleme özgü kullanıcı onayı al.
- CLI örneği: `python -m kobi_akis crm --contacts examples/contacts.csv --deals examples/deals.csv --today 2026-10-14 --output out/crm.md`.
