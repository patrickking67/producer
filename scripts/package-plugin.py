"""Build dist/producer.plugin from plugins/producer/.

The archive is reproducible: files come from git (tracked and untracked but
not ignored), are sorted, get a fixed timestamp and mode, and are stored
without compression so the bytes do not depend on the zlib build. Building
twice from the same source gives the same bytes on any machine, so the
repository check can compare the committed bundle with a fresh build.

Usage:
  python3 scripts/package-plugin.py           write dist/producer.plugin
  python3 scripts/package-plugin.py --check   exit 1 if dist/ is out of date
"""

from pathlib import Path
import io
import subprocess
import sys
import zipfile


root = Path(__file__).resolve().parents[1]
source = "plugins/producer"
archive_path = root / "dist" / "producer.plugin"
fixed_time = (1980, 1, 1, 0, 0, 0)


def source_files():
    listed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", source],
        cwd=root,
        capture_output=True,
        check=True,
    ).stdout.decode()
    paths = sorted({path for path in listed.split("\0") if path})
    return [path for path in paths if (root / path).is_file()]


def build():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for path in source_files():
            info = zipfile.ZipInfo(path[len(source) + 1:], date_time=fixed_time)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            archive.writestr(info, (root / path).read_bytes())
    return buffer.getvalue()


def main():
    data = build()
    if "--check" in sys.argv[1:]:
        if not archive_path.exists() or archive_path.read_bytes() != data:
            print("dist/producer.plugin is out of date: run python3 scripts/package-plugin.py")
            return 1
        print("dist/producer.plugin matches plugins/producer/")
        return 0
    archive_path.parent.mkdir(exist_ok=True)
    archive_path.write_bytes(data)
    print(f"Packaged {archive_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
