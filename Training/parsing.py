# Author : Richard Delwin Myloth

from Training.Git_Cmds import get_bugfix_commits, link_fixes_to_bugs

def get_labels():

    """

    This function is used to get the those commit id of those commits which would have previously introduced bugs
    :return: A list of commit id which are found to be buggy

    """

    fix_commits = get_bugfix_commits()

    bug_commits = link_fixes_to_bugs(fix_commits)

    return bug_commits