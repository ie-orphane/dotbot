import os

import env
from utils import File, Log

DATA = {
    "dirs": ["users"],
    "files": {
        "[]": ["evaluations"],
    },
    "tables": [
        ("interactions", "datetime,id,name,command,options"),
    ],
}
STORAGE = [
    "files",
    "subjects",
    "solutions",
    "logs",
    "evaluations",
    "errors",
]
CONFIG = {
    "global": {
        int: ["GUILD"],
        dict: ["EMOJIS"],
    },
}


def run() -> None:
    base_dir = os.path.abspath(env.BASE_DIR)

    for base in ("data", "storage", "config", "backup"):
        os.makedirs(os.path.join(base_dir, base), exist_ok=True)

    for dir in DATA["dirs"]:
        dir_path = os.path.join(base_dir, "data", dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            Log.info("Data", f"Dir {os.path.relpath(dir_path)} created.")

    for content, files in DATA["files"].items():
        for file in files:
            file_path = os.path.join(base_dir, "data", f"{file}.json")
            try:
                with open(file_path, "x") as f:
                    f.write(content)
                    Log.info("Data", f"File {os.path.relpath(file_path)} created.")
            except FileExistsError:
                pass

    for table_name, table_header in DATA["tables"]:
        table_path = os.path.join(base_dir, "data", f"{table_name}.csv")
        try:
            with open(table_path, "x") as f:
                f.write(table_header.replace("\n", "") + "\n")
                Log.info("Data", f"Table {os.path.relpath(table_path)} created.")
        except FileExistsError:
            pass

    for store in STORAGE:
        store_path = os.path.join(base_dir, "storage", store)
        if not os.path.exists(store_path):
            os.makedirs(store_path)
            Log.info("Storage", f"{os.path.relpath(store_path)} created.")

    for config, attrs in CONFIG.items():
        config_path = os.path.join(base_dir, "config", f"{config}.json")
        try:
            with open(config_path, "x") as f:
                f.write("{}")
                Log.info("Config", f"{os.path.relpath(config_path)} created.")
        except FileExistsError:
            pass

        configs: dict = File.read(config_path)
        changed: bool = False

        for attr_type, attributes in attrs.items():
            for attribute in attributes:
                if attribute not in configs:
                    configs[attribute] = attr_type()
                    changed = True

        if changed:
            File.write(config_path, configs)
