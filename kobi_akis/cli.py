"""Sentetik veya kullanıcının izin verdiği yerel dosyalardan yalnızca rapor üretir."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sys


class InputError(ValueError):
    """Doğrulanamayan kayıt veya argüman."""


def _rows(path: Path, required: set[str]) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            found = set(reader.fieldnames or [])
            missing = sorted(required - found)
            if missing:
                raise InputError(f"{path.name}: eksik sütunlar: {', '.join(missing)}")
            result = []
            for number, item in enumerate(reader, start=2):
                if None in item or any(value is None for value in item.values()):
                    raise InputError(f"{path.name}:{number}: hatalı CSV satırı")
                result.append({key: str(value).strip() for key, value in item.items()})
            return result
    except (OSError, UnicodeError, csv.Error) as exc:
        raise InputError(f"{path}: okunamadı ({exc})") from exc


def _date(raw: str, label: str) -> date:
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise InputError(f"{label}: YYYY-MM-DD biçiminde tarih gerekli") from exc


def _md(raw: str) -> str:
    """Keep external CSV values out of Markdown control syntax."""
    clean = re.sub(r"[\x00-\x1f\x7f]", " ", str(raw))
    return clean.replace("\\", "\\\\").replace("|", "\\|").replace("`", "\\`").replace("<", "&lt;").replace(">", "&gt;")


def report_invoices(path: Path, today: date) -> str:
    rows = _rows(path, {"invoice_id", "customer", "email", "amount", "currency", "due_date", "status"})
    overdue: list[dict] = []
    by_currency: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for line, row in enumerate(rows, start=2):
        status = row["status"].casefold()
        if status in {"paid", "cancelled", "canceled", "void", "ödendi", "iptal"}:
            continue
        if status not in {"open", "unpaid", "overdue", "açık", "ödenmedi", "gecikmiş"}:
            raise InputError(f"{path.name}:{line}: bilinmeyen fatura durumu: {status!r}")
        try:
            amount = Decimal(row["amount"])
        except InvalidOperation as exc:
            raise InputError(f"{path.name}:{line}: geçersiz tutar") from exc
        if not amount.is_finite() or amount < 0:
            raise InputError(f"{path.name}:{line}: tutar negatif veya sonlu olmayan değer olamaz")
        currency = row["currency"].upper()
        if not re.fullmatch(r"[A-Z]{3}", currency):
            raise InputError(f"{path.name}:{line}: 3 harfli para birimi gerekli")
        due = _date(row["due_date"], f"{path.name}:{line}")
        days = (today - due).days
        if days <= 0:
            continue
        by_currency[currency] += amount
        overdue.append({**row, "amount_value": amount, "currency": currency, "days": days})
    overdue.sort(key=lambda rec: (-rec["days"], rec["invoice_id"]))
    lines = ["# Gecikmiş faturalar — inceleme raporu", "", f"Rapor tarihi: {today.isoformat()}",
             "", f"Gecikmiş fatura adedi: **{len(overdue)}**", "",
             "Para birimine göre toplam (farklı para birimleri birleştirilmez):"]
    lines += [f"- {code}: {value:.2f}" for code, value in sorted(by_currency.items())] or ["- Gecikmiş tutar bulunmadı."]
    lines += ["", "| Fatura | Müşteri | Vade | Gecikme (gün) | Tutar |",
              "| --- | --- | --- | ---: | ---: |"]
    for rec in overdue:
        lines.append(f"| {_md(rec['invoice_id'])} | {_md(rec['customer'])} | {rec['due_date']} | {rec['days']} | {rec['amount_value']:.2f} {rec['currency']} |")
    lines += ["", "## Gönderilmeyen hatırlatma taslakları", "",
              "**Dikkat:** Bunlar otomatik e-posta değildir. Adres ve tutarları doğrulamadan göndermeyin.", ""]
    for rec in overdue:
        lines += [f"### Fatura {_md(rec['invoice_id'])}", "",
                  f"Alıcı (kontrol edin): {_md(rec['email']) or '[eksik]'}", "",
                  f"Merhaba {_md(rec['customer'])},", "",
                  f"{_md(rec['invoice_id'])} numaralı, {rec['amount_value']:.2f} {rec['currency']} tutarındaki faturamızın vadesi {rec['due_date']} tarihinde dolmuştur. Ödeme durumunu teyit edebilir misiniz? Ödeme yapıldıysa lütfen bu mesajı dikkate almayın.", "",
                  "Teşekkürler.", "", "---", ""]
    return "\n".join(lines).rstrip() + "\n"


def report_crm(contacts: Path, deals: Path, today: date) -> str:
    people = _rows(contacts, {"contact_id", "name", "email", "phone"})
    opportunities = _rows(deals, {"deal_id", "name", "stage", "owner", "last_activity_date"})
    groups: dict[str, list[str]] = defaultdict(list)
    incomplete = []
    for rec in people:
        email = rec["email"].casefold()
        if email:
            groups[email].append(rec["contact_id"])
        if not rec["name"] or not rec["email"]:
            incomplete.append(rec)
    duplicates = sorted(((k, v) for k, v in groups.items() if len(v) > 1), key=lambda x: x[0])
    stale = []
    no_owner = []
    for line, rec in enumerate(opportunities, start=2):
        if not rec["owner"]:
            no_owner.append(rec["deal_id"])
        if rec["stage"].casefold() in {"won", "lost", "closed", "closed won", "closed lost", "kazanıldı", "kaybedildi"}:
            continue
        if not rec["last_activity_date"]:
            stale.append((rec["deal_id"], "aktivite tarihi eksik"))
            continue
        last = _date(rec["last_activity_date"], f"{deals.name}:{line}")
        days = (today - last).days
        if days > 30:
            stale.append((rec["deal_id"], f"{days} gün hareketsiz"))
    lines = ["# CRM veri kalitesi — inceleme raporu", "", f"Rapor tarihi: {today}", "",
             "**Hiçbir kişi birleştirilmedi veya CRM güncellenmedi.**", "",
             "## Aynı normalize e-postayı kullanan kişi kayıtları", ""]
    lines += [f"- {_md(email)}: {', '.join(map(_md, ids))}" for email, ids in duplicates] or ["- Bulunmadı."]
    lines += ["", "## Eksik temel kişi alanları", ""]
    lines += [f"- {_md(rec['contact_id'])}: eksik {', '.join(key for key in ('name', 'email') if not rec[key])}" for rec in incomplete] or ["- Bulunmadı."]
    lines += ["", "## Eksik fırsat sahipleri", ""]
    lines += [f"- {_md(item)}" for item in no_owner] or ["- Bulunmadı."]
    lines += ["", "## Durgun açık fırsatlar (>30 gün) veya eksik tarih", ""]
    lines += [f"- {_md(key)}: {_md(note)}" for key, note in stale] or ["- Bulunmadı."]
    lines += ["", "Bunlar **inceleme önerileri**dir. Aynı e-posta her zaman aynı kişi anlamına gelmeyebilir."]
    return "\n".join(lines) + "\n"


KEYWORDS = {
    "Otomatik yenileme": ("otomatik yenilen", "automatic renewal", "auto-renew"),
    "Cezai şart": ("cezai şart", "penalty clause", "liquidated damages"),
    "Sorumluluk sınırı": ("sorumluluk sınır", "limitation of liability"),
    "Tek taraflı fesih": ("tek taraflı fesih", "unilateral termination"),
    "Veri işleme": ("kişisel veri", "data processing", "gdpr", "kvkk"),
}


def report_contract(path: Path) -> str:
    if path.suffix.lower() not in {".txt", ".md"}:
        raise InputError("Sözleşme girdisi UTF-8 .txt veya .md olmalı; PDF/DOCX desteği yok")
    try:
        if path.stat().st_size > 1_000_000:
            raise InputError("Bu demo en fazla 1 MB sözleşme metni kabul eder")
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise InputError(f"{path}: okunamadı ({exc})") from exc
    lower = content.casefold()
    lines = ["# Sözleşme ön inceleme kontrol listesi", "",
             "**Bu araç hukuki analiz yapmaz; anahtar kelimeleri işaretleyen bir demodur.**", "",
             f"Kaynak: `{_md(path.name)}`", "", "## İncelenecek başlıklar", ""]
    for label, words in KEYWORDS.items():
        matches = [word for word in words if word in lower]
        lines.append(f"- **{label}**: " + ("anahtar ifade bulundu — bağlamı hukuk uzmanına gösterin" if matches else "anahtar ifade bulunmadı — bu hükmün olmadığı anlamına gelmez"))
    lines += ["", "## İnsan kontrolü gereken konular", "",
              "- Tarafların kimliği, imza yetkileri, uygulanacak hukuk ve yetkili mahkeme", 
              "- Ücret, ödeme zamanı, fesih usulü, gizlilik ve kişisel verilerin işlenmesi", 
              "- İlgili alan uzmanı/avukat tarafından inceleme ve onay", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Çevrimdışı KOBİ rapor demosu; dış sisteme hiçbir işlem yapmaz")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("invoices", help="Gecikmiş faturalar ve hatırlatma taslakları")
    a.add_argument("--input", required=True, type=Path)
    a.add_argument("--today", default=date.today().isoformat())
    a.add_argument("--output", required=True, type=Path)
    b = sub.add_parser("crm", help="CRM kalite kontrolü")
    b.add_argument("--contacts", required=True, type=Path)
    b.add_argument("--deals", required=True, type=Path)
    b.add_argument("--today", default=date.today().isoformat())
    b.add_argument("--output", required=True, type=Path)
    c = sub.add_parser("contract", help="Basit sözleşme anahtar kelime kontrolü")
    c.add_argument("--input", required=True, type=Path)
    c.add_argument("--output", required=True, type=Path)
    args = p.parse_args(argv)
    try:
        if args.cmd == "invoices":
            result = report_invoices(args.input, _date(args.today, "--today"))
        elif args.cmd == "crm":
            result = report_crm(args.contacts, args.deals, _date(args.today, "--today"))
        else:
            result = report_contract(args.input)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
        print(f"Rapor kaydedildi: {args.output}")
        return 0
    except (InputError, OSError) as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 2
