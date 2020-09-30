# Author : Richard Delwin Myloth

import re
from collections import defaultdict
from subprocess import check_output


def run_bash_command(bash_cmd):

    stdout = check_output(bash_cmd.split()).decode('utf-8').rstrip('\n')
    return stdout


def trim_hash(commit):

    return commit[:8]


def get_latest_commit():

    bash_cmd = 'git log -1 --pretty=format:"%H"'

    stdout = run_bash_command(bash_cmd)

    # single line outputs get quoted by check_output for some reason
    stdout = stdout.replace('"', '')

    return trim_hash(stdout)


def get_bugfix_commits():

    bash_cmd = "git log -i --all --grep BUG --grep FIX --pretty=format:%h"

    stdout = run_bash_command(bash_cmd)

    # filter out empty strings
    commits = [commit for commit in stdout.split('\n') if commit]

    if not commits:
        raise ValueError('No bug fix commits found')

    return commits


def _get_commit_filenames(commit_hash):


    commit_hash = trim_hash(commit_hash)

    bash_cmd = ('git --no-pager diff {commit_hash} {commit_hash}^ --name-only'
                .format(commit_hash=commit_hash))

    stdout = run_bash_command(bash_cmd)

    # note that .split() always returns a list, even if the string wasn't split
    filenames = stdout.split('\n')

    return filenames


def _get_commit_lines(commit_hash, filenames):


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