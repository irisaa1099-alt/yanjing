"""Start the Windows portable workspace with its own database cluster."""
import gzip
import json
import msvcrt
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time
from urllib.request import urlopen

runtime = Path(__file__).resolve().parent
app = runtime.parent / "research-lens"
state = app / ".local"
sys.path.insert(0, str(runtime))
from pg_paths import postgres_root
port = int(os.environ.get("YANJING_PORT", "18765"))
pgport = int(os.environ.get("YANJING_PG_PORT", "55469"))
url = f"http://127.0.0.1:{port}"

os.chdir(app)
sys.path.insert(0, str(app))
os.environ.update(
    YANJING_STATE=str(state), YANJING_PG_PORT=str(pgport),
    YANJING_OLLAMA_BIN=str(runtime / "ollama" / "ollama.exe"),
    OLLAMA_MODELS=str(runtime / "models"), OLLAMA_NO_CLOUD="1",
)
os.environ.setdefault("YANJING_OLLAMA_BASE_URL", "http://127.0.0.1:11439/v1")
os.environ.pop("YANJING_DATABASE_URL", None)

import uvicorn


def occupied(number):
    with socket.socket() as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", number)) == 0


def show_page():
    for _ in range(180):
        try:
            with urlopen(url + "/api/health", timeout=2) as response:
                if json.load(response).get("app") == "research-lens":
                    print(f"研镜已就绪  {url}")
                    if os.environ.get("YANJING_NO_BROWSER") != "1":
                        os.startfile(url)
                    return
        except OSError:
            pass
        time.sleep(0.5)


def main():
    state.mkdir(exist_ok=True)
    with (state / "portable.lock").open("a+b") as lock:
        lock.seek(0)
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            print("此副本已经启动。")
            show_page()
            return
        if occupied(port):
            raise SystemExit(f"网页端口 {port} 已被占用。请设置 YANJING_PORT 指定空闲端口。")
        with postgres_root(runtime.parent) as pg_root:
            serve(pg_root)


def serve(pg_root):
    pgbin = pg_root / "runtime" / "postgres" / "bin"
    pg_state = pg_root / "research-lens" / ".local"
    os.environ["YANJING_PORTABLE_PG_ROOT"] = str(pg_root)
    os.environ["PATH"] = os.pathsep.join(
        [str(pg_root / "runtime" / "python"), str(pgbin), os.environ["PATH"]]
    )
    from db import connect, start_postgres

    cluster = pg_state / "pgdata"
    ctl = [str(pgbin / "pg_ctl.exe"), "-D", str(cluster)]
    running = cluster.exists() and subprocess.run(
        [*ctl, "status"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ).returncode == 0
    if occupied(pgport) and not running:
        raise SystemExit(f"数据库端口 {pgport} 已被占用。请设置 YANJING_PG_PORT 指定空闲端口。")
    print("正在打开研镜，首次启动将恢复随包论文库。")
    start_postgres()
    try:
        with connect() as conn:
            if not conn.execute("SELECT to_regclass('public.catalog_head') AS t").fetchone()["t"]:
                with gzip.open(runtime / "catalog.sql.gz", "rt", encoding="utf-8") as dump:
                    conn.execute(dump.read(), prepare=False)
        threading.Thread(target=show_page, daemon=True).start()
        uvicorn.run("app:app", host="127.0.0.1", port=port)
    finally:
        subprocess.run([*ctl, "-m", "fast", "-w", "stop"], check=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
