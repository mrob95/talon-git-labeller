
from setuptools import setup
import os
import talon_git_labeller


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="talon_git_labeller",
    description="Adds items to a talon list when certain git commands are executed, allowing files to be easily selected by voice.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Mike Roberts",
    url="https://github.com/mrob95/talon-git-labeller",
    project_urls={
        "Issues": "https://github.com/mrob95/talon_git_labeller/issues",
    },
    license="MIT",
    version=talon_git_labeller.__VERSION__,
    packages=["talon_git_labeller"],
    entry_points="""
        [console_scripts]
        git-tl-branch=talon_git_labeller.cli:main
        git-tl-status=talon_git_labeller.cli:main
        git-tl-stash-pop=talon_git_labeller.cli:main
    """,
    python_requires=">=3.7",
)
