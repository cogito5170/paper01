#!/usr/bin/env bash
# 공개 저장소에서 뺀 논문 PDF를 papers/MANIFEST.tsv에 따라 내려받는다.
# 사용: 저장소 루트에서 `bash scripts/fetch_papers.sh` (이미 있는 파일은 건너뜀)
# arXiv·공개 URL은 자동으로 받고, 유료 논문(manual)은 목록만 출력한다.
set -u
cd "$(dirname "$0")/.."

MANIFEST=papers/MANIFEST.tsv
UA="Mozilla/5.0 (paper01 fetch_papers.sh)"
got=$(mktemp)    # 같은 출처를 여러 경로가 쓰면 한 번만 받고 복사 (url<TAB>path)
trap 'rm -f "$got"' EXIT
manual=()
ok=0; skip=0; fail=0

fetch() {  # fetch <url> <dest>
  local tmp; tmp=$(mktemp)
  if curl -sfL -m 120 -A "$UA" -o "$tmp" "$1" && [ "$(head -c 4 "$tmp")" = "%PDF" ]; then
    mkdir -p "$(dirname "$2")"; mv "$tmp" "$2"; return 0
  fi
  rm -f "$tmp"; return 1
}

while IFS=$'\t' read -r path src note; do
  [[ -z "$path" || "$path" == \#* ]] && continue
  if [ -s "$path" ]; then skip=$((skip+1)); continue; fi
  if [ "$src" = manual ]; then manual+=("$path${note:+  ($note)}"); continue; fi

  case "$src" in
    arxiv:*) url="https://arxiv.org/pdf/${src#arxiv:}" ;;
    *)       url="$src" ;;
  esac

  prev=$(awk -F'\t' -v u="$url" '$1==u{print $2; exit}' "$got")
  if [ -n "$prev" ]; then
    mkdir -p "$(dirname "$path")"; cp "$prev" "$path"
  elif fetch "$url" "$path"; then
    printf '%s\t%s\n' "$url" "$path" >> "$got"
    [[ "$src" == arxiv:* ]] && sleep 3   # arXiv 요청 간격 권고
  else
    echo "실패: $path <- $url"; fail=$((fail+1)); continue
  fi
  echo "받음: $path"; ok=$((ok+1))
done < "$MANIFEST"

# 번역 작업용 원문 텍스트 (PDF에서 다시 만든다)
if command -v pdftotext >/dev/null; then
  f=derivations/translation_enttsel2026/src
  [ -s $f/orig.pdf ] || cp papers/segment/EnttselCorlay2026_ModelAwareRD.pdf $f/orig.pdf 2>/dev/null
  [ -s $f/orig.pdf ] && [ ! -s $f/orig.txt ] && pdftotext $f/orig.pdf $f/orig.txt
  f=derivations/translation_seon2026_comst/src
  [ -s $f/orig.pdf ] && [ ! -s $f/orig.txt ] && pdftotext $f/orig.pdf $f/orig.txt
  f=derivations/translation
  [ -s download/2504.07743.pdf ] && [ ! -s $f/source.txt ] && pdftotext -layout download/2504.07743.pdf $f/source.txt
else
  echo "pdftotext가 없어 원문 텍스트(orig.txt, source.txt)는 만들지 않았다 (brew install poppler)."
fi

echo
echo "받음 $ok, 이미 있음 $skip, 실패 $fail"
if [ ${#manual[@]} -gt 0 ]; then
  echo "유료·비공개라 직접 받아야 하는 논문 ${#manual[@]}편 (학교 IEEE Xplore 등):"
  printf '  %s\n' "${manual[@]}"
fi
