"""Provide an ASCII path to the original portable folder for PostgreSQL on Windows."""
from contextlib import contextmanager
import ctypes
import os
from pathlib import Path
import subprocess
import tempfile
import _winapi


@contextmanager
def postgres_root(folder):
    if str(folder).isascii():
        yield folder
        return

    short = ctypes.create_unicode_buffer(32768)
    size = ctypes.windll.kernel32.GetShortPathNameW(str(folder), short, len(short))
    if 0 < size < len(short) and short.value.isascii():
        alias = Path(short.value)
        if alias.is_dir() and alias.samefile(folder):
            yield alias
            return

    # Some NTFS volumes have no 8.3 names. A private junction also works there.
    temp = Path(tempfile.gettempdir())
    if str(temp).isascii():
        with tempfile.TemporaryDirectory(prefix="yanjing-pg-", dir=temp) as work:
            link = Path(work) / "package"
            try:
                _winapi.CreateJunction(str(folder), str(link))
            except OSError:
                pass
            else:
                try:
                    yield link
                finally:
                    link.rmdir()  # Remove the junction itself, never its contents.
                return

    # A Chinese user profile can put both the package and TEMP on non-ASCII paths.
    subst = Path(os.environ["SystemRoot"]) / "System32" / "subst.exe"
    for code in range(ord("Z"), ord("D") - 1, -1):
        letter = chr(code) + ":"
        drive = Path(letter + "\\")
        if ctypes.windll.kernel32.GetLogicalDrives() & (1 << (code - ord("A"))):
            continue
        result = subprocess.run([subst, letter, str(folder)], capture_output=True)
        if result.returncode:
            continue
        try:
            if drive.is_dir() and drive.samefile(folder):
                yield drive
                return
        finally:
            # Only remove a drive still pointing at the directory we mapped.
            if drive.is_dir() and drive.samefile(folder):
                subprocess.run([subst, letter, "/D"], check=True)
    raise RuntimeError("PostgreSQL 无法取得此目录的英文路径。请释放一个盘符后重试。")
