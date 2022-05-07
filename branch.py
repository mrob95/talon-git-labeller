from typing import Dict
from utils import dump_list_file, sort_out_windows_colours, map_numbers_to_spoken, run_command
import re
import sys
import platform

GIT_BRANCH_ITEMS_LIST    = "git_branch_items"

if platform.system().lower() == "windows":
    sort_out_windows_colours()

COLOUR_GREEN = "\x1b[32m"
COLOUR_RESET = "\x1b[0m"

def git_branch() -> Dict[str, str]:
    out = run_command(["git", "branch"])

    branch_map = {}

    for branch_num, line in enumerate(out.rstrip().split("\n"), 1):
        if line.startswith("*"):
            # Current branch
            branch = re.match(r"\*\s(.+?)$", line).group(1).strip()
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
    assert len(sys.argv) == 2, "Usage: branch.py {talon list file location}"
    branch_map = git_branch()
    dump_list_file(sys.argv[1], GIT_BRANCH_ITEMS_LIST, branch_map)
