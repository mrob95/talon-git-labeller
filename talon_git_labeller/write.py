from pathlib import Path
from typing import Dict

LIST_FILE_TEMPLATE = """
from talon import Module, Context

mod = Module()
ctx = Context()

mod.list("{list_name}")

ctx.lists["user.{list_name}"] = {items}

"""

def dump_list_file(location: Path, list_name: str, items: Dict):
    with open(location, "w") as f:
        f.write(LIST_FILE_TEMPLATE.format(list_name=list_name, items=items))
