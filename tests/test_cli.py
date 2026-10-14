import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from kobi_akis.cli import InputError, main, report_contract, report_crm, report_invoices

ROOT = Path(__file__).resolve().parents[1]


class ReportTests(unittest.TestCase):
    def test_invoice_filters_and_currency(self):
        text = report_invoices(ROOT / 'examples/invoices.csv', date(2026, 10, 14))
        self.assertIn('Gecikmiş fatura adedi: **2**', text)
        self.assertIn('TRY: 1250.00', text)
        self.assertIn('EUR: 400.00', text)
        self.assertNotIn('INV-003', text)
        self.assertNotIn('INV-004', text)
        self.assertIn('Gönderilmeyen hatırlatma taslakları', text)

    def test_crm_only_exact_emails_marked(self):
        text = report_crm(ROOT / 'examples/contacts.csv', ROOT / 'examples/deals.csv', date(2026, 10, 14))
        self.assertIn('C-001, C-002', text)
        self.assertIn('D-001: 70 gün hareketsiz', text)
        self.assertIn('D-004: aktivite tarihi eksik', text)
        self.assertNotIn('D-003: ', text)
        self.assertIn('D-002', text)

    def test_contract_is_plain_heuristic(self):
        text = report_contract(ROOT / 'examples/sample-contract.txt')
        self.assertIn('hukuki analiz yapmaz', text)
        self.assertIn('anahtar ifade bulundu', text)

    def test_bad_invoices_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.csv'
            path.write_text('invoice_id,customer,email,amount,currency,due_date,status\nA,B,c,NaN,TRY,2026-01-01,open\n', encoding='utf-8')
            with self.assertRaises(InputError):
                report_invoices(path, date(2026, 10, 14))

    def test_cli_creates_report_not_email(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'nested' / 'out.md'
            code = main(['invoices', '--input', str(ROOT / 'examples/invoices.csv'), '--today', '2026-10-14', '--output', str(target)])
            self.assertEqual(code, 0)
            self.assertTrue(target.is_file())

    def test_manifest_skills_have_frontmatter(self):
        manifest = json.loads((ROOT / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['name'], 'kobi-is-akislari')
        for skill in (ROOT / 'skills').glob('*/SKILL.md'):
            content = skill.read_text(encoding='utf-8')
            self.assertTrue(content.startswith('---\nname: '), skill)


if __name__ == '__main__':
    unittest.main()
