import logging
import sys
import re
from typing import Any

import structlog


def _mask_pii(text: str) -> str:
    """Mask common PII patterns in a string: emails, phones, CPF/CNPJ-like numbers."""
    if not text:
        return text
    masked = text
    # Email
    masked = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[email_masked]", masked)
    # Phone numbers (simple BR-ish patterns, keep last 2 digits)
    masked = re.sub(r"(?:(?:\+?55)?\s*\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}", "[phone_masked]", masked)
    # CPF (###.###.###-##) and digits only
    masked = re.sub(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "[cpf_masked]", masked)
    masked = re.sub(r"\b\d{11}\b", "[cpf_masked]", masked)
    # CNPJ (##.###.###/####-##) and digits only
    masked = re.sub(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", "[cnpj_masked]", masked)
    masked = re.sub(r"\b\d{14}\b", "[cnpj_masked]", masked)
    return masked


class PiiMaskingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            # Mask the formatted message content
            if record.args:
                # Force message formatting so getMessage picks args
                msg = record.getMessage()
                record.msg = _mask_pii(msg)
                record.args = ()
            else:
                record.msg = _mask_pii(str(record.msg))
        except Exception:
            # Never break logging
            pass
        return True


def configure_logging(level: int = logging.INFO) -> None:
    """Configure structlog + stdlib logging for JSON output and contextvars.

    This function is safe to call multiple times (idempotent).
    """

    timestamper = structlog.processors.TimeStamper(fmt="iso")
    pre_chain = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        timestamper,
    ]

    def pii_processor(logger, method_name, event_dict):
        # Mask string values in structlog events
        try:
            for k, v in list(event_dict.items()):
                if isinstance(v, str):
                    event_dict[k] = _mask_pii(v)
        except Exception:
            pass
        return event_dict

    structlog.configure(
        processors=[
            *pre_chain,
            pii_processor,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure root stdlib logging to go to stdout
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.addFilter(PiiMaskingFilter())
        handler.setFormatter(logging.Formatter("%(message)s"))
        root.addHandler(handler)

    root.setLevel(level)


__all__ = ["configure_logging"]
