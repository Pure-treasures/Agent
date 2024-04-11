import logging
import sys
import os
import threading
from typing import Optional

_lock = threading.Lock()
_default_handler: Optional[logging.Handler] = None

LoggerName = "agent-server"

from logging import (
    CRITICAL,  # NOQA
    DEBUG,  # NOQA
    ERROR,  # NOQA
    FATAL,  # NOQA
    INFO,  # NOQA
    NOTSET,  # NOQA
    WARN,  # NOQA
    WARNING,  # NOQA
)


log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# 定义颜色转义序列
COLOR_SEQ = "\033[1;%dm"
COLOR_END_SEQ = "\033[0m"

# 定义颜色常量
COLORS = {
    'DEBUG': '36',  # 青色
    'INFO': '32',   # 绿色
    'WARNING': '33',  # 黄色
    'ERROR': '31',  # 红色
    'CRITICAL': '35'  # 紫色
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        seq = COLOR_SEQ % int(COLORS.get(levelname, '0'))
        message = super().format(record)
        message = message.replace(levelname, f"{seq}{levelname}{COLOR_END_SEQ}")
        return message
    
_default_log_level = logging.INFO

def _get_default_logging_level():
    """
    If TRANSFORMERS_VERBOSITY env var is set to one of the valid choices return that as the new default level. If it is
    not - fall back to `_default_log_level`
    """
    env_level_str = os.getenv("AUTOML_VERBOSITY", None)
    if env_level_str:
        if env_level_str in log_levels:
            return log_levels[env_level_str]
        else:
            logging.getLogger().warning(
                f"Unknown option AUTOML_VERBOSITY={env_level_str}, "
                f"has to be one of: { ', '.join(log_levels.keys()) }"
            )
    return _default_log_level

def _get_default_formatter():
    return ColorFormatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y/%d/%m %H:%M:%S" 
    )

def _get_library_name() -> str:
    return __name__.split(".")[0]


def _get_library_root_logger() -> logging.Logger:
    return logging.getLogger(_get_library_name())


def _configure_library_root_logger() -> None:
    
    global _default_handler

    with _lock:
        if _default_handler:
            # This library has already configured the library root logger.
            return
        _default_handler = logging.StreamHandler()  # Set sys.stderr as stream.
        _default_handler.flush = sys.stderr.flush
        _default_handler.setFormatter(_get_default_formatter())
        
        # Apply our default configuration to the library root logger.
        library_root_logger = _get_library_root_logger()
        library_root_logger.addHandler(_default_handler)
        library_root_logger.setLevel(_get_default_logging_level())
        library_root_logger.propagate = False

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a logger with the specified name.
    """

    if name is None:
        name = _get_library_name()

    _configure_library_root_logger()
    return logging.getLogger(name)
