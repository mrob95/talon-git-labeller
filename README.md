# Git item labeller for Talon
These scripts replace git commands, numbering items in the output and creating a talon list of the items so they can be referred to with voice commands. For example:
```
$ git_status
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
2. Declare lists in your user directory to accept the data
3. Open `status.py` and set the `GIT_STATUS_ITEMS_CONTEXT` and `GIT_STATUS_ITEMS_LIST` variables. For example if I have `user/apps/terminal/git.py` containing `mod.list("git_status_items")` then they should be `user.apps.terminal.git` and `git_status_items` respectively. You can get a list of all contexts by calling `registry.contexts` in the REPL.
4. Create a bash alias to run `status.py`, e.g. `alias "git_status"="python3 ~/path/status.py"`
5. Create some commands to use the list of items, e.g.
```
git status: "git_status\n"
git {user.git_actions} {user.git_status_items} [(and {user.git_status_items})+]:
	items = user.cat(git_status_items_list, "' '")
	"git {git_actions} '{items}'"
git go {user.git_status_items}: user.cd_directory_of(git_status_items)
git file {user.git_status_items}: "'{git_status_items}'"
```