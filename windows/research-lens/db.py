import os
import secrets
import shutil
import subprocess
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

ROOT = Path(__file__).resolve().parent
STATE = Path(os.getenv("YANJING_STATE", ROOT / ".local"))
PORT = int(os.getenv("YANJING_PG_PORT", "55462"))


PORTABLE_PG_ROOT = os.getenv("YANJING_PORTABLE_PG_ROOT")


def pg_tool(name):
    if os.name == "nt":
        bundled = Path(PORTABLE_PG_ROOT or ROOT.parent) / "runtime" / "postgres" / "bin" / (name + ".exe")
        if bundled.is_file():
            return str(bundled)
    else:
        bundled = ROOT / "node_modules/@embedded-postgres/darwin-arm64/native/bin" / name
    executable = shutil.which(name) or (str(bundled) if bundled.is_file() else None)
    if not executable:
        raise RuntimeError(f"缺少 {name}，请安装 PostgreSQL 或配置专用 YANJING_DATABASE_URL。")
    return executable


def connect(**options):
    if os.getenv("YANJING_DATABASE_URL"):
        return psycopg.connect(os.environ["YANJING_DATABASE_URL"], row_factory=dict_row, **options)
    return psycopg.connect(
        host="127.0.0.1",
        port=PORT,
        dbname="postgres",
        user="yanjing",
        password=(STATE / "pgpass").read_text().strip(),
        row_factory=dict_row, **options,
    )


def start_postgres():
    if os.getenv("YANJING_DATABASE_URL"):
        return
    STATE.mkdir(mode=0o700, exist_ok=True)
    pg_state = Path(PORTABLE_PG_ROOT) / "research-lens" / ".local" if PORTABLE_PG_ROOT else STATE
    cluster = pg_state / "pgdata"
    auth = pg_state / "pgpass"
    if not (cluster / "PG_VERSION").exists():
        if not auth.exists():
            auth.touch(mode=0o600)
            auth.write_text(secrets.token_hex(32))
        subprocess.run(
            [
                pg_tool("initdb"),
                "-D",
                cluster,
                "-U",
                "yanjing",
                "--pwfile",
                auth,
                "--auth=scram-sha-256",
                "--encoding=UTF8",
                "--locale=C",
            ],
            check=True,
        )
    ctl = [pg_tool("pg_ctl"), "-D", cluster]
    if subprocess.run([*ctl, "status"], stdout=subprocess.DEVNULL).returncode:
        subprocess.run(
            [
                *ctl,
                "-w",
                "-l",
                pg_state / "postgres.log",
                "-o",
                f"-h 127.0.0.1 -p {PORT}" + ("" if os.name == "nt" else " -c unix_socket_directories=''"),
                "start",
            ],
            check=True,
        )
