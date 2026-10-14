# GitHub'a herkese açık olarak yayımlama

GitHub'da yeni repo oluşturma izni olan bir oturum gereklidir. Bu kitin başka bir hesabın mevcut deposuna yanlışlıkla gönderilmemesi için hedef depo açıkça belirlenir.

## En kısa yol (GitHub CLI)

1. [GitHub CLI](https://cli.github.com/) kurun ve `gh auth login` ile kendi hesabınızda oturum açın.
2. Bu klasörde bir terminal açın ve çalıştırın:

```bash
bash scripts/publish.sh GITHUB_KULLANICI_ADI/kobi-is-akislari
```

Betik `kobi-is-akislari` adlı **public** repo oluşturur ve mevcut klasörü `main` dalına push eder. GitHub'da böyle bir repo zaten varsa hata verir; var olan repoyu üzerine yazmaz.

## Alternatif (GitHub web arayüzü)

1. GitHub'da **New repository** ile `kobi-is-akislari` adlı **Public** boş repo oluşturun. README, lisans, .gitignore kutularını işaretlemeyin (bunlar kitte var).
2. İndirdiğiniz arşivi açıp klasörde aşağıdaki komutları çalıştırın:

```bash
git init -b main
git add .
git commit -m "Initial open-source KOBI workflows starter"
git remote add origin https://github.com/GITHUB_KULLANICI_ADI/kobi-is-akislari.git
git push -u origin main
```

## Yayımlama öncesi kontrol

- Yalnızca örnek/sentetik veriler var mı? `git status` ve `git diff --cached --name-only` ile denetleyin.
- `python -m unittest discover -s tests -v` başarılı mı?
- `LICENSE`, `NOTICE`, `SECURITY.md` ve `CREDITS.md` korunuyor mu?
- GitHub deposunun görünürlüğü **Public** mı?
- Gerçek hesapların erişim tokenları, özel belgeler veya müşteri verileri var mı? Varsa **push etmeyin**.
