"""Central logging boundary for framework and security-test modules."""

from __future__ import annotations

import logging
import sys
from typing import TextIO


_DEFAULT_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s] - %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Return a named logger without configuring handlers."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    return logging.getLogger(name.strip())


def configure_logging(
    level: int = logging.INFO,
    *,
    stream: TextIO | None = None,
) -> None:
    """Configure console logging once without duplicating existing handlers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if root_logger.handlers:
        return

    handler = logging.StreamHandler(stream if stream is not None else sys.stderr)
    handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
    root_logger.addHandler(handler)


__all__ = [
    "configure_logging",
    "get_logger",
]
