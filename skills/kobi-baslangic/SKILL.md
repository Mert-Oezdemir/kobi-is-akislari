---
name: kobi-baslangic
description: Türkçe KOBİ iş akışı başlangıç kontrolü; işletme ihtiyacını belirler, izinleri doğrular ve ilk güvenli denemeyi planlar. "Kuruluma başla", "ilk otomasyon" ve "beni başlat" isteklerinde kullan.
---

# KOBİ iş akışlarına başlangıç

1. Önce tek bir tekrarlanan iş sorununu belirle: gecikmiş faturalar, CRM veri kalitesi, sözleşme ön okuması veya müşteri şikâyeti.
2. Bu iş için gereken en az veri alanlarını belirt; gerçek müşteri verisi gerekmedikçe `examples/` içindeki sentetik dosyalarla başla.
3. Kullanıcının erişimi olmayan bir araca bağlandığını iddia etme. Var olan bağlayıcıları ve izinlerini açıkça teyit et; kullanıcının kendisinin hesap erişimi vermesini iste.
4. Önce yalnızca okunabilir özet üret. Eksik tutar, işlem durumu, tarih veya izin varsa tahmin yürütme.
5. Yapılacak her eylemi somut biçimde sırala ve taslakları göster; harici gönderim, para transferi, silme, imza veya kayıt güncellemesi için **eyleme özgü açık onay** almadan ilerleme.
6. Hangi veri okundu, ne üretildi, ne onay bekliyor kısa bir kayıtla bitir.

Bu beceri API erişimi sağlamaz ve resmî Anthropic Small Business eklentisi değildir.
