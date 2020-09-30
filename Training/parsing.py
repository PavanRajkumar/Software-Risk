# Author : Richard Delwin Myloth

from Git_Cmds import get_bugfix_commits, link_fixes_to_bugs

def get_labels():

    fix_commits = get_bugfix_commits()

    bug_commits = link_fixes_to_bugs(fix_commits)

    return bug_commits