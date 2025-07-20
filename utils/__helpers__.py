import json
import os
from datetime import UTC, datetime
from typing import Literal

from .__colorful__ import Color as clr

__all__ = [
    "convert_seconds",
    "log",
    "File",
    "open_file",
]

def open_file(file_path, data=None):
    if data:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)
            return

    with open(file_path, "r") as file:
        return json.load(file)

def convert_seconds(total_seconds: int) -> str:
    time_units = [
        ("y", 365 * 24 * 3600),
        ("mo", 30 * 24 * 3600),
        ("d", 24 * 3600),
        ("h", 3600),
        ("min", 60),
        ("s", 1),
    ]

    result = []
    for label, unit in time_units:
        if total_seconds >= unit:
            value, total_seconds = divmod(total_seconds, unit)
            result.append(f"{value}{label}")

    return " ".join(result)


def log(
    type: Literal["Info", "Error", "Task"],
    color: Literal["red", "green", "yellow", "blue", "cyan"],
    name: str,
    message: str,
):
    print(
        clr.black(datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")),
        f"{getattr(clr, color)(type)}{' ' * (8 - len(type))}",
        clr.magenta(name),
        message,
    )


class File:
    @staticmethod
    def read(file_path: str):
        with open(file_path) as file:
            return json.load(file)

    @staticmethod
    def write(file_path: str, data):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def get(path: str, parser=int):
        return [parser(file[: file.index(".")]) for file in os.listdir(path)]
