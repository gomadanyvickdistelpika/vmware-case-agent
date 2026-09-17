from dataclasses import dataclass
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    database_path: Path = PROJECT_ROOT / "data" / "memory.db"
    knowledge_dir: Path = PROJECT_ROOT / "knowledge"
    max_upload_bytes: int = int(os.getenv("DANY_MAX_UPLOAD_MB", "10")) * 1024 * 1024


settings = Settings()

