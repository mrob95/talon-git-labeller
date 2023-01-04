from pathlib import Path
import subprocess
from typing import List
import os

from talon_git_labeller.const import PLATFORM


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


def run_command(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True)
    out = proc.stdout.decode("utf-8")
    err = proc.stderr.decode("utf-8")
    # Can these be mixed?
    return out or err


def get_talon_user_path() -> Path:
    if PLATFORM == "linux":
        with open("/proc/version") as f:
            is_wsl = "microsoft" in f.read()
        if is_wsl:
            windows_appdata = run_command(["cmd.exe", "/C", "echo %APPDATA%"]).strip()
            unix_appdata = run_command(["wslpath", windows_appdata]).strip()
            user_dir = Path(unix_appdata) / "talon" / "user"
        else:
            user_dir = Path("~/.talon/user")
    elif PLATFORM == "darwin":
        user_dir = Path("~/.talon/user")
    elif PLATFORM == "windows":
        user_dir = Path(os.path.expandvars("%APPDATA%/talon/user"))
    else:
        raise NotImplementedError(f"Unexpected platform '{PLATFORM}'")
    return user_dir


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
