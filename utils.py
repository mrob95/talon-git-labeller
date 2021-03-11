import subprocess
import platform
from typing import Dict, List
import os, sys

DEBUG = False or os.getenv("DEBUG")
OUT = None if DEBUG else subprocess.DEVNULL

def sort_out_windows_colours():
    # https://bugs.python.org/issue29059
    from ctypes import windll, c_int, byref
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    STD_OUTPUT_HANDLE = c_int(-11)
    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    mode = c_int(0)
    windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
    mode = c_int(mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)


raw_digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
raw_teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]

digits = {i: name for i, name in enumerate(raw_digits)}
teens = {i: name for i, name in enumerate(raw_teens, 10)}

def map_numbers_to_spoken(n: int) -> str:
    if n <= 9:
        return digits[n]
    elif 10 <= n <= 19:
        return teens[n]
    else: # TODO
        text = " ".join([digits[int(digit)] for digit in str(n)])
        return text


if platform.system().lower() == "windows":
    TALON_RESOURCES = os.path.join(os.path.expandvars("%APPDATA%"), "talon", ".venv", "Scripts", ".resources")
    TALON_DIR = open(TALON_RESOURCES, "r").read().strip()
    TALON_PYTHON = os.path.join(TALON_DIR, "python.exe")
    TALON_REPL = os.path.join(TALON_DIR, "repl.py")
    def run_talon(cmds: List[str]):
        cmd = "\n".join(cmds) + "\n"
        subprocess.run([TALON_PYTHON, TALON_REPL], input=cmd.encode("utf-8"), stdout=OUT)
else:
    TALON_REPL = os.path.expanduser("~/.talon/bin/repl")
    def run_talon(cmds: List[str]):
        cmd = "\n".join(cmds) + "\n"
        subprocess.run([TALON_REPL], input=cmd.encode("utf-8"), stdout=OUT)


def set_list(context: str, list_name: str, contents: Dict):
    cmd = [
        f"ctx = registry.contexts['{context}']",
        f"ctx.lists['user.{list_name}'] = {contents}",
    ]
    if DEBUG:
        cmd.append(f"print(ctx.lists['user.{list_name}'])")
    run_talon(cmd)

def run_command(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True)
    out = proc.stdout.decode("utf-8")
    return out