"""
@author : Richard Delwin Myloth, Pavan Rajkumar
"""
import re
from collections import defaultdict
from subprocess import check_output


def run_bash_command(bash_cmd):

    """
    To execute the git bash command

    :param bash_cmd: The git bash commmand executed to get the commit details.
    :return:  The result of the bash command executed which is split and decoded.
    """

    stdout = check_output(bash_cmd.split()).decode('utf-8').rstrip('\n')
    return stdout


def trim_hash(commit):
    """
    Trims commit's hash id
    :param commit: commit id
    :return: commit id trimmed to first 8 places
    """

    return commit[:8]


def get_latest_commit():
    """
    To get the latest commit, this commit is not used since it is used in the
    python script located in .git/git_hooks directory to execute this.

    :return: git output of the latest commit details
    """

    bash_cmd = 'git log -1 --pretty=format:"%H"'

    stdout = run_bash_command(bash_cmd)

    # single line outputs get quoted by check_output for some reason
    stdout = stdout.replace('"', '')

    return trim_hash(stdout)


def get_bugfix_commits():

    """
    This function is used to obtain all the commit id which have BUG or FIX in their commit messages which indicate
    that, that particular commit was used to fix a bug which was identified.

    Raises ValueError if not buggy commits are found. This may be due to the fact that the repository might be a small one,
    or the commit messages are not approprately labelled as BUG or FIX

    :return: List of commit ids which fixed a bug
    """

    bash_cmd = "git log -i --all --grep BUG --grep FIX --pretty=format:%h"

    stdout = run_bash_command(bash_cmd)

    # filter out empty strings
    commits = [commit for commit in stdout.split('\n') if commit]

    if not commits:
        raise ValueError('No bug fix commits found')

    return commits


def _get_commit_filenames(commit_hash):

    """
    This function is used to get the files which were affected by a commit id.

    :param commit_hash: commit id
    :return: list of filenames

    """

    commit_hash = trim_hash(commit_hash)

    bash_cmd = ('git --no-pager diff {commit_hash} {commit_hash}^ --name-only'
                .format(commit_hash=commit_hash))

    stdout = run_bash_command(bash_cmd)

    # note that .split() always returns a list, even if the string wasn't split
    filenames = stdout.split('\n')

    return filenames


def _get_commit_lines(commit_hash, filenames):
    """
    The function is used to obtain the lines which were modified by the commit id in that particular file given by the filename
    :param commit_hash: commit id
    :param filenames: list of filenames modified by commit id
    :return: Lines affected
    """

    commit_hash = trim_hash(commit_hash)
    fname_lines = defaultdict(lambda: [])

    for fname in filenames:

        bash_cmd = ('git --no-pager diff {commit}^ {commit} -U0 -- {fname}'
                    .format(commit=commit_hash, fname=fname))

        stdout = run_bash_command(bash_cmd)

        # pull out the header line of each diff section
        headers = [l for l in stdout.split('\n') if '@@' in l]

        # header will look like @@ -198,2 +198,2 @@
        for header in headers:

            # the .group(1) bit will pull out the part prefixed by '+'
            match = re.match('@@ -(.*) +(.*) @@', header).group(1)

            # header looks like @@ -198 +198 @@ if only one line changes
            if ',' in match:
                start, n_lines = match.split(',')
            else:
                start, n_lines = match, '1'

            if int(n_lines) > 0:
                fname_lines[fname].append((start, n_lines))

    return fname_lines


def _get_blame_commit(commit_hash, filenames, fname_lines):

    """
    This function is used to obtain the commit id (buggy commits) responsible for introducing lines which were
    changed in the file (filenames) by the commit id (commit_hash).

    :param commit_hash: commit id
    :param filenames: files modifies by commit_hash
    :param fname_lines: lines modified in the file (i.e. filenames)
    :return: commit ids which introduced the bug
    """


    commit_hash = trim_hash(commit_hash)
    buggy_commits = set()

    for fname in filenames:

        for start, n_lines in fname_lines[fname]:

            bash_cmd = \
                ('git --no-pager blame -L{start},+{n} {commit}^ -- {fname}'
                 .format(start=start,
                         n=n_lines,
                         commit=commit_hash,
                         fname=fname))

            stdout = run_bash_command(bash_cmd)

            changed_lines = stdout.split('\n')
            buggy_commits = \
                buggy_commits.union([l.split(' ')[0] for l in changed_lines])

    return buggy_commits


def link_fixes_to_bugs(fix_commits):

    """
    This function is used to find those commits responsible for introducing bugs into the software

    :param fix_commits: list of commit ids obtained from Git_Cmds.get_bugfix_commits() which
                        indicate the commits which were used to fix a bug (type - list of Strings)
    :return: List of commit ids which introduces the bug
    """


    bug_commits = set()

    for commit in fix_commits:

        # trim the hash to 8 characters
        commit = trim_hash(commit)

        # get the files modified by the commit
        filenames = _get_commit_filenames(commit)

        # get the lines in each file modified by the commit
        fname_lines = _get_commit_lines(commit, filenames)

        # get the last commit to modify those lines
        origin_commits = _get_blame_commit(commit, filenames, fname_lines)

        bug_commits = bug_commits.union(origin_commits)

    return list(bug_commits)