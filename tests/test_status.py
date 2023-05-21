from talon_git_labeller.commands import parse_status, COLOUR_GREEN, COLOUR_RED, COLOUR_RESET

def test_status_ignore_rebase():
    out = """
Last commands done (2 commands done):
   pick 57de123 b
   e 129c34b d
No commands remaining.
You are currently editing a commit while rebasing branch 'master' on '8b86a4d'.
  (use "git commit --amend" to amend the current commit)
  (use "git rebase --continue" once you are satisfied with your changes)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
\tmodified:   a

no changes added to commit (use "git add" and/or "git commit -a")
"""
    lines, file_map = parse_status(out)
    assert file_map == {
        "one": "a",
    }

def test_status_unmerged_paths():
    out = """
On branch b1
Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
\tboth modified:   b

no changes added to commit (use "git add" and/or "git commit -a")
"""
    lines, file_map = parse_status(out)
    assert file_map == {
        "one": "b",
    }

def test_status_rename():
    out = """
On branch b1
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
\trenamed:    c -> z
"""
    lines, file_map = parse_status(out)
    assert file_map == {
        "one": "z",
    }

def test_untracked():
    out = """
On branch b1
Untracked files:
  (use "git add <file>..." to include in what will be committed)
\ta b
\th

nothing added to commit but untracked files present (use "git add" to track)
"""
    lines, file_map = parse_status(out)
    assert file_map == {
        "one": "a b",
        "two": "h",
    }

def test_colours():
    out = """
On branch b1
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
\trenamed:    c -> z

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
\tmodified:   b
"""
    expected = f"""
On branch b1
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
   1.   {COLOUR_GREEN}renamed:    c -> z{COLOUR_RESET}

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
   2.   {COLOUR_RED}modified:   b{COLOUR_RESET}
"""
    lines, file_map = parse_status(out)
    assert file_map == {
        "one": "z",
        "two": "b",
    }
    assert "\n".join(lines) == expected.strip()
