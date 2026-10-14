#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! "$1" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then
  echo 'Kullanım: bash scripts/publish.sh KULLANICI_ADI/kobi-is-akislari' >&2
  exit 2
fi
if ! command -v gh >/dev/null 2>&1; then
  echo 'GitHub CLI eksik: https://cli.github.com/' >&2
  exit 2
fi
if ! command -v git >/dev/null 2>&1; then
  echo 'Git kurulmalı.' >&2
  exit 2
fi
gh auth status >/dev/null
repo="$1"
if gh repo view "$repo" >/dev/null 2>&1; then
  echo "Hedef depo zaten var: $repo. Üzerine yazılmıyor." >&2
  exit 2
fi
cd "$(dirname "$0")/.."
if [[ ! -d .git ]]; then git init -b main; fi
if git remote get-url origin >/dev/null 2>&1; then
  echo 'Bu klasörde origin zaten ayarlı. Değişiklik yapılmadı.' >&2
  exit 2
fi
if [[ -z "$(git config user.name || true)" || -z "$(git config user.email || true)" ]]; then
  echo 'Önce git config user.name ve user.email ayarlarını yapın.' >&2
  exit 2
fi
python -m unittest discover -s tests -v
printf '\nYayımlanacak dosyalar:\n'
git add .
git diff --cached --name-only
printf '\nGerçek müşteri verisi/anahtar bulunmadığını kontrol edin. Devam? [y/N] '
read -r confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo 'İptal edildi.'
  exit 1
fi
if ! git diff --cached --quiet; then git commit -m "Initial open-source KOBI workflows starter"; fi
gh repo create "$repo" --public --source=. --remote=origin --push
