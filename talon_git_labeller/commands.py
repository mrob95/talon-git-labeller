from typing import List, Dict
import sys
import re

from talon_git_labeller.helpers import run_command, map_numbers_to_spoken


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
