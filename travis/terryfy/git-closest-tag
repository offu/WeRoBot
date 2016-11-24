#!/usr/bin/env python
# vim: ft=python
""" Get tag with fewest commits from path of given branch

Usage:

    git-closest-tag [commit-ish]

To get closest tag to current HEAD

    git-closest-tag

To get closest tag to origin/master

    git-closest-tag origin/master

What does "closest" mean, in "closest tag"?

Imagine the following git history::

    A->B->C->D->E->F (HEAD)
           \     \
            \     X->Y->Z (v0.2)
             P->Q (v0.1)

Imagine the developer tag'ed Z as v0.2 on Monday, and then tag'ed Q as v0.1 on
Tuesday. v0.1 is the more recent, but v0.2 is closer in development history to
HEAD, in the sense that the path it is on starts at a point closer to HEAD.

We may want get the tag that is closer in development history. We can find that
by using ``git log v0.2..HEAD`` etc for each tag. This gives you the number of
commits on HEAD since the path ending at v0.2 diverged from the path followed by
HEAD.

``git describe`` does something slightly different, in that it tracks back from
(e.g.) HEAD to find the first tag that is on a path back in the history from
HEAD. In git terms, ``git describe`` looks for tags that are "reachable" from
HEAD.  It will therefore not find tags like v0.2 that are not on the path back
from HEAD, but a path that diverged from there.
"""
# Requires at least Python 2.7
from __future__ import print_function

import sys
from subprocess import check_output


def backtick(cmd):
    """ Get command output as stripped string """
    output = check_output(cmd)
    return output.decode('latin1').strip()


def tagged_commit(tag):
    return backtick(['git', 'rev-parse', '--verify', tag + '^{commit}'])


def n_commits_exclude_include(exclude, include):
    commit_range = '{}..{}'.format(exclude, include)
    commits = backtick(['git', 'log', '--oneline', commit_range])
    return 0 if commits == '' else len(commits.split('\n'))


def main():
    # Get commit-ish from passed command arguments, HEAD is default
    try:
        target_ref = sys.argv[1]
    except IndexError:
        target_ref = 'HEAD'
    # SHA1 for target reference
    target_commit = tagged_commit(target_ref)
    tag_lines = backtick(['git', 'tag'])
    if tag_lines == '':
        raise RuntimeError("No tags to compare")
    tags = [tag.strip() for tag in tag_lines.split('\n')]
    tags_info = {}
    min_after = float('inf')
    for tag in tags:
        tag_commit = tagged_commit(tag)
        # The commits along target branch since the root of the branch that the
        # tag is on
        merge_base = backtick(['git', 'merge-base', tag, target_commit])
        tags_info[tag] = (tag_commit, merge_base)
        n_after = n_commits_exclude_include(merge_base, target_commit)
        if n_after < min_after:
            min_after = n_after
            candidates = [tag]
        elif n_after == min_after:
            candidates.append(tag)
    if len(candidates) == 0:
        raise RuntimeError('Could not find any useful tags')
    if len(candidates) == 1:
        print(candidates[0])
        return
    # More than one candidate with same post-tag-on-target length
    max_post_common = -1
    for tag in candidates:
        tag_commit, merge_base = tags_info[tag]
        n_after = n_commits_exclude_include(merge_base, tag_commit)
        if n_after > max_post_common:
            closest_tag = tag
            max_post_common = n_after
    print(closest_tag)


if __name__ == '__main__':
    main()
