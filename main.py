from typing import Dict, List
import re
import os, sys
import platform
import subprocess


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

if platform.system().lower() == "windows":
    sort_out_windows_colours()


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

LIST_FILE_TEMPLATE = """
from talon import ui, Module, Context, registry, actions, imgui, cron, clip

mod = Module()
ctx = Context()

mod.list("{list_name}")

ctx.lists["user.{list_name}"] = {items}

"""

def dump_list_file(location: str, list_name: str, items: Dict):
    with open(location, "w") as f:
        f.write(LIST_FILE_TEMPLATE.format(list_name=list_name, items=items))

GIT_BRANCH_ITEMS_LIST = "git_branch_items"
GIT_STATUS_ITEMS_LIST = "git_status_items"

COLOUR_GREEN = "\x1b[32m"
COLOUR_RED   = "\x1b[31m"
COLOUR_RESET = "\x1b[0m"


def git_status(cmd: List[str]) -> Dict[str, str]:
    COLOUR_MAP = {
        "Changes to be committed:": COLOUR_GREEN,
        "Changes not staged for commit:": COLOUR_RED,
        "Untracked files:": COLOUR_RED,
        "Unmerged paths:": COLOUR_RED,
    }

    out = run_command(["git", *cmd])

    file_num = 1
    file_map = {}
    colour = ""

    for line in out.strip().split("\n"):
        if line in COLOUR_MAP:
            colour = COLOUR_MAP[line]

        contains_file = re.match(r"^\s+[^(\s]", line)
        if contains_file:
            # first group is e.g. 'modified:' or 'deleted:'
            file_name_match = re.match(r"^\s+([a-z\s]+:\s+)?(.+?)( \(.+?\))?$", line)
            if file_name_match:
                file_name = file_name_match.group(2)
                spoken = map_numbers_to_spoken(file_num)
                file_map[spoken] = file_name
                print(f"  {file_num: >2}.   {colour}{line.strip()}{COLOUR_RESET}")
                file_num += 1
            else:
                # Shouldn't ever hit this, means the regexes are missing something
                print(line)
        else:
            print(line)

    sys.stdout.flush()
    return file_map


def git_branch() -> Dict[str, str]:
    out = run_command(["git", "branch"])

    branch_map = {}

    for branch_num, line in enumerate(out.rstrip().split("\n"), 1):
        if line.startswith("*"):
            # Current branch
            branch = line.lstrip("*").strip()
            line_to_print = f"* {COLOUR_GREEN}{branch}{COLOUR_RESET}"
        else:
            branch = line.strip()
            line_to_print = line
        spoken = map_numbers_to_spoken(branch_num)
        branch_map[spoken] = branch
        print(f" {branch_num: >2}. {line_to_print}")
        branch_num += 1

    sys.stdout.flush()
    return branch_map


if __name__ == '__main__':
    assert len(sys.argv) == 3, "Usage: branch.py {git command} {talon list file location}"
    cmd, target = sys.argv[1], sys.argv[2]
    if cmd == "branch":
        branch_map = git_branch()
        dump_list_file(target, GIT_BRANCH_ITEMS_LIST, branch_map)
    elif cmd == "status":
        file_map = git_status(["status"])
        dump_list_file(target, GIT_STATUS_ITEMS_LIST, file_map)
    elif cmd == "stash_pop":
        file_map = git_status(["stash", "pop"])
        dump_list_file(target, GIT_STATUS_ITEMS_LIST, file_map)
    else:
        raise ValueError(f"Unrecognised command {cmd}")
