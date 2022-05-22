
set_title() {
    echo -ne "\033]0;$1\a"
}

labeller_path="~/talon-git-labeller/main.py"
talon_user_path="/mnt/c/Users/Mike/AppData/Roaming/talon/user"

git() {
    if [ "$1" == "add" ] && [ "$2"  == "-p" ]; then
        set_title "--- Git patching ---"
        $(which git) "$@"
    elif [ "$1" == "checkout" ] && [ "$2"  == "-p" ]; then
        set_title "--- Git patching ---"
        $(which git) "$@"
    elif [ "$1" == "status" ] && [ "$#" == "1" ]; then
        python3.9 "$labeller_path" status "$talon_user_path/git_pt/status.py"
    elif [ "$1" == "branch" ] && [ "$#" == "1" ]; then
        python3.9 "$labeller_path" branch "$talon_user_path/git_pt/branch.py"
    else
        $(which git) "$@"
    fi
}
