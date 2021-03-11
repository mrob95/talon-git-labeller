from utils import sort_out_windows_colours, map_numbers_to_spoken, set_list, run_command
import re
import platform
import sys


GIT_STATUS_ITEMS_CONTEXT = "user.apps.terminal.git"
GIT_STATUS_ITEMS_LIST    = "git_status_items"

if platform.system().lower() == "windows":
    sort_out_windows_colours()

out = run_command(["git", "status"])

COLOUR_GREEN = "\x1b[32m"
COLOUR_RED   = "\x1b[31m"
COLOUR_RESET = "\x1b[0m"
colour_map = {
    "Changes to be committed:": COLOUR_GREEN,
    "Changes not staged for commit:": COLOUR_RED,
    "Untracked files:": COLOUR_RED,
    "Unmerged paths:": COLOUR_RED,
}

file_num = 1
file_map = {}
colour = ""

for line in out.strip().split("\n"):
    if line in colour_map:
        colour = colour_map[line]

    contains_file = re.match(r"^\s+[^(\s]", line)
    if contains_file:
        # first group is e.g. 'modified:' or 'deleted:'
        file_name_match = re.match(r"^\s+([a-z\s]+:\s+)?(.+?)$", line)
        if file_name_match:
            file_name = file_name_match.group(2).strip("/")
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

set_list(GIT_STATUS_ITEMS_CONTEXT, GIT_STATUS_ITEMS_LIST, file_map)