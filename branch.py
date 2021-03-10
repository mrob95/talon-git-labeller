from utils import sort_out_windows_colours, map_numbers_to_spoken, set_list, run_command
import re
import platform

GIT_STATUS_ITEMS_CONTEXT = "user.apps.terminal.git"
GIT_STATUS_ITEMS_LIST    = "git_branch_items"

if platform.system().lower() == "windows":
    sort_out_windows_colours()

out = run_command(["git", "branch"])

COLOUR_GREEN = "\x1b[32m"
COLOUR_RESET = "\x1b[0m"

branch_num = 1
branch_map = {}
colour = ""

for line in out.strip().split("\n"):
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

set_list(GIT_STATUS_ITEMS_CONTEXT, GIT_STATUS_ITEMS_LIST, branch_map)