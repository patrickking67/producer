#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/plugins/producer"
archive="$repo_root/dist/producer.plugin"
temporary_archive="$(mktemp "${TMPDIR:-/tmp}/producer.XXXXXX.zip")"

trap 'rm -f "$temporary_archive"' EXIT
rm -f "$temporary_archive"
mkdir -p "$repo_root/dist"

(
  cd "$source_dir"
  zip -q -r -X "$temporary_archive" .
)

mv "$temporary_archive" "$archive"
trap - EXIT
echo "Packaged $archive"
