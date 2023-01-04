# Git item labeller for Talon
![Talon labeller demo gif](https://raw.githubusercontent.com/mrob95/talon-git-labeller/master/images/demo.gif)

These scripts replace git commands, numbering items in the output and creating a talon list of the items so they can be referred to with voice commands. For example:
```
$ git tl-status
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
1. Install [pipx](https://pypa.github.io/pipx/):
```
pip3 install pipx
```
2. Install the `talon_git_labeller` package globally:
```
pipx install talon_git_labeller
```
3. Switch to using the new git commands:
    * `git status` -> `git tl-status`
    * `git branch` -> `git tl-branch`
    * `git stash pop` -> `git tl-stash-pop`
4. Create some commands to use the `git_status_items` and `git_branch_items` lists in talon, e.g.:
```
git status: "git tl-status\n"
git add {user.git_status_items}: "git add '{git_status_items}'"
git diff {user.git_status_items}: "git diff '{git_status_items}'"
git file {user.git_status_items}: "'{git_status_items}'"

git branch: "git tl-branch\n"
git checkout {user.git_branch_items}: "git checkout '{git_branch_items}'"
```
5. Use the commands by saying e.g. "git add one".
