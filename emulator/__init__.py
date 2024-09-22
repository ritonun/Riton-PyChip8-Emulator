import logging

logging.basicConfig(
    filename="emulator.log",
    encoding="utf-8",
    filemode="w",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
)
logging.info("")
logging.info("--- START ---")
