import logging
from pathlib import Path


class LoggingConfig:
    @staticmethod
    def configure(
        log_level: int = logging.INFO,
        log_dir: str = "logs",
        log_file: str = "trading_bot.log",
    ) -> None:
        root_logger = logging.getLogger()
        if root_logger.handlers:
            return

        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler(log_path / log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        root_logger.setLevel(log_level)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)
