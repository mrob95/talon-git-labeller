from typing import List, Dict, Tuple
import sys
import re

from talon_git_labeller.const import PLATFORM
from talon_git_labeller.helpers import run_command, map_numbers_to_spoken, sort_out_windows_colours


COLOUR_GREEN = "\x1b[32m"
COLOUR_RED   = "\x1b[31m"
COLOUR_RESET = "\x1b[0m"

def parse_status(out: str) -> Tuple[List[str], Dict[str, str]]:
    COLOUR_MAP = {
        "Changes to be committed:": COLOUR_GREEN,
        "Changes not staged for commit:": COLOUR_RED,
        "Untracked files:": COLOUR_RED,
        "Unmerged paths:": COLOUR_RED,
    }

    lines = []
    file_map = {}
    file_num = 1
    colour = ""

    for line in out.strip().split("\n"):
        if line in COLOUR_MAP:
            colour = COLOUR_MAP[line]

        # first group is e.g. 'modified:' or 'deleted:'
        file_name_match = re.match(r"^\t([a-z\s]+:\s+)?(.+?)( \(.+?\))?$", line)
        if file_name_match:
            file_name = file_name_match.group(2)
            if file_name_match.group(1) and file_name_match.group(1).strip() == "renamed:":
                _, _, file_name = file_name.rpartition(" -> ")
            spoken = map_numbers_to_spoken(file_num)
            file_map[spoken] = file_name
            lines.append(f"  {file_num: >2}.   {colour}{line.strip()}{COLOUR_RESET}")
            file_num += 1
        else:
            lines.append(line)

    return lines, file_map


def git_status(cmd: List[str]) -> Dict[str, str]:
    out = run_command(["git", *cmd])
    if PLATFORM == "windows":
        sort_out_windows_colours()

    lines, file_map = parse_status(out)
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()
    return file_map


def git_branch() -> Dict[str, str]:
    out = run_command(["git", "branch"])
    if PLATFORM == "windows":
        sort_out_windows_colours()

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
