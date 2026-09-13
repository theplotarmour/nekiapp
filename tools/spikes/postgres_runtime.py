"""Own an isolated loopback PostgreSQL cluster; never use an existing service/DSN."""

import os
from pathlib import Path
import shutil
import socket
import subprocess
from uuid import uuid4


class PostgresRuntime:
    def __init__(self, bin_dir):
        self.bin_dir = Path(bin_dir).resolve()
        self.base = Path(__file__).resolve().parent / ".postgres-runtime"
        self.root = self.base / uuid4().hex
        self.data = self.root / "data"
        self.user = "neki_probe"
        self.started = False
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            self.port = sock.getsockname()[1]

    def run(self, executable, *args):
        suffix = ".exe" if os.name == "nt" else ""
        # Windows server children can inherit a pipe and keep communicate() open
        # after pg_ctl exits. A file allows waiting for the actual command only.
        log = self.root / ("command-" + uuid4().hex + ".log")
        with log.open("w", encoding="utf8") as output:
            result = subprocess.run(
                [str(self.bin_dir / (executable + suffix)), *map(str, args)],
                stdout=output, stderr=subprocess.STDOUT, text=True, timeout=60,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
        result.stdout = log.read_text(encoding="utf8", errors="replace")
        result.check_returncode()
        return result

    @property
    def dsn(self):
        return f"host=127.0.0.1 port={self.port} dbname=postgres user={self.user} connect_timeout=5"

    def start(self):
        self.root.mkdir(parents=True, exist_ok=False)
        self.run("initdb", "-D", self.data, "-U", self.user,
                 "--auth=trust", "--encoding=UTF8", "--locale=C")
        # If launch times out, cleanup must still check/stop our possible server.
        self.started = True
        self.run("pg_ctl", "-D", self.data, "-l", self.root / "server.log",
                 "-o", f"-h 127.0.0.1 -p {self.port}", "-w", "start")
        return self

    def restart(self):
        self.run("pg_ctl", "-D", self.data, "-m", "fast", "-w", "restart")

    def close(self):
        if self.started:
            if (self.data / "postmaster.pid").exists():
                self.run("pg_ctl", "-D", self.data, "-m", "fast", "-w", "stop")
            self.started = False
        # Resolve both paths before recursive cleanup; only our UUID child qualifies.
        root = self.root.resolve()
        base = self.base.resolve()
        if root.parent != base or len(root.name) != 32:
            raise RuntimeError("Refusing cleanup outside the isolated runtime root")
        if root.exists():
            shutil.rmtree(root)
