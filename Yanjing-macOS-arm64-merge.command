#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
out="Yanjing-macOS-arm64.zip"
if [[ -e "$out" ]]; then echo "Already exists: $out"; exit 1; fi
tmp=$(mktemp "./.Yanjing-XXXXXXXX")
trap 'rm -f -- "$tmp"' EXIT
for i in $(seq 1 6); do
  part=$(printf '%s.%03d' "$out" "$i")
  [[ -f "$part" ]] || { echo "Missing: $part"; exit 1; }
  cat "$part" >> "$tmp"
done
digest=$(shasum -a 256 "$tmp")
[[ "${digest%% *}" == "174f926778ed0eb3f1fd02b0f437ed7dafb2ee11a0c59cd7bad897d1e6b9df8c" ]] || { echo "SHA-256 mismatch. Download the parts again."; exit 1; }
ln "$tmp" "$out"
echo "Verified $out"
