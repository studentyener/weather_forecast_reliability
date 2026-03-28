from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = ROOT_DIR / "outputs"

for directory in (DATA_DIR, DATA_PROCESSED_DIR, OUTPUTS_DIR):
    directory.mkdir(parents=True, exist_ok=True)
