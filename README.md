# Git item labeller for Talon
![Talon labeller demo gif](images/demo.gif)

These scripts replace git commands, numbering items in the output and creating a talon list of the items so they can be referred to with voice commands. For example:
```
$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)

   1.   .gitignore
   2.   README.md
   3.   status.py
   4.   utils.py

nothing added to commit but untracked files present (use "git add" to track)
```
with the following items being added to a list:
```
{'one': '.gitignore', 'two': 'README.md', 'three': 'status.py', 'four': 'utils.py'}
```

## Instructions
1. Clone this repo somewhere other than your talon user directory
2. Create shell aliases to run main.py, passing the git command (branch or status) and the path to a python file in your user directory where the list will be written. e.g. (set your own `labeller_path` and `talon_user_path` here)
```
labeller_path="$ZPLUGINDIR/talon-git-labeller/main.py"
talon_user_path="/mnt/c/Users/Mike/AppData/Roaming/talon/user/git-labeller"
mkdir -p $talon_user_path
function git() {
    if [ "$1" = "status" ] && [ "$#" = "1" ]; then
        python "$labeller_path" status "$talon_user_path/status.py"
    elif [ "$1" = "stash" ] && [ "$2" = "pop" ] && [ "$#" = "2" ]; then
        python "$labeller_path" stash_pop "$talon_user_path/status.py"
    elif [ "$1" = "branch" ] && [ "$#" = "1" ]; then
        python "$labeller_path" branch "$talon_user_path/branch.py"
    else
        command git "$@"
    fi
}
```
3. Create some commands to use the `git_status_items` and `git_branch_items` lists, e.g.:
```
git status: "git_status\n"
git add {user.git_status_items} [(and {user.git_status_items})+]:
	items = user.cat(git_status_items_list, "' '")
	"git {git_actions} '{items}'"
git go {user.git_status_items}: user.cd_directory_of(git_status_items)
git file {user.git_status_items}: "'{git_status_items}'"
```
