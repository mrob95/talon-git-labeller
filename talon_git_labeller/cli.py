from pathlib import Path
import sys

from talon_git_labeller.commands import git_branch, git_status
from talon_git_labeller.const import PLATFORM, USER_SUBFOLDER, GIT_BRANCH_ITEMS_LIST, GIT_STATUS_ITEMS_LIST
from talon_git_labeller.helpers import get_talon_user_path, sort_out_windows_colours
from talon_git_labeller.write import dump_list_file


def main():
    exe = Path(sys.argv[0])
    cmd = exe.name

    user_dir = get_talon_user_path()
    if not user_dir.exists():
        raise ValueError(f"Expected to find talon user directory at '{user_dir}', but didn't")
    labeller_dir = user_dir / USER_SUBFOLDER
    labeller_dir.mkdir(exist_ok=True)

    if PLATFORM == "windows":
        sort_out_windows_colours()

    if cmd == "git-tl-branch":
        target = labeller_dir / "branch.py"
        branch_map = git_branch()
        dump_list_file(target, GIT_BRANCH_ITEMS_LIST, branch_map)
    elif cmd == "git-tl-status":
        target = labeller_dir / "status.py"
        file_map = git_status(["status"])
        dump_list_file(target, GIT_STATUS_ITEMS_LIST, file_map)
    elif cmd == "git-tl-stash-pop":
        target = labeller_dir / "status.py"
        file_map = git_status(["stash", "pop"])
        dump_list_file(target, GIT_STATUS_ITEMS_LIST, file_map)
    else:
        raise ValueError(f"Unrecognised command {cmd}")
