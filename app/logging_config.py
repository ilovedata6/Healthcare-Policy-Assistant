import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Log directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


def configure_logging() -> None:
    """
    Configure root logger with:
      - RotatingFileHandler (5 MB per file, keep 5 backups)
      - Console handler (stdout)
      - Conventional formatter for both file and console
    Call this once at application startup.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Formatter for both console and file (conventional)
    log_fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_fmt)
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = RotatingFileHandler(
        filename=str(LOG_FILE),
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_fmt)
    root_logger.addHandler(file_handler)


# Expose a logger for modules to use:
# from app.logging_config import logger
configure_logging()
logger = logging.getLogger("healthcare_policy_assistant")
