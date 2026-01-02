import json
import os
import subprocess
import tempfile
from pathlib import Path

from astro_engine.models import AstrologicalData, HouseSystem

MODULE_DIR = Path(__file__).resolve().parent
SWISS_BIN = MODULE_DIR / "swecli" / "main"


def get_chart(
    date: str,
    time: str,
    latitude: float,
    longitude: float,
    house_system: HouseSystem,
    timezone_IANA_id: str,
) -> AstrologicalData:
    # Make an output file path
    fd, out_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)

    cmd = [
        str(SWISS_BIN),
        "--date",
        date,
        "--time",
        time,
        "--lat",
        f"{latitude}",
        "--lon",
        f"{longitude}",
        "--hsys",
        house_system.value,
        "--tzid",
        timezone_IANA_id,
        "--json",
        out_path,
    ]

    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)

    print("Exit code:", res.returncode)
    if res.stdout:
        print("STDOUT:\n", res.stdout)
    if res.stderr:
        print("STDERR:\n", res.stderr)

    if res.returncode != 0:
        raise RuntimeError("C binary failed (see output above)")

    if os.path.getsize(out_path) == 0:
        raise RuntimeError("JSON output file is empty (did you pass --json PATH?)")

    try:
        with open(out_path, "r", encoding="utf-8") as f:
            return AstrologicalData.model_validate(json.load(f))
    finally:
        try:
            os.remove(out_path)
        except OSError:
            pass
