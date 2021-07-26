import argparse
import re
from typing import AbstractSet
from typing import Optional, \
    Union
from typing import Sequence

from pre_commit_hooks.util import CalledProcessError
from pre_commit_hooks.util import cmd_output


def get_issue_key() -> Union[str, None]:
    """ looks for an issue key given the 
        smart commit convention of <branch-type>/<issue-key>/<description>
        Returns:
            the key if found else None
    """
    try:
        ref = cmd_output('git', 'symbolic-ref', 'HEAD')
    except CalledProcessError:
        return None
    branch_parts = ref.split('/')[2:]

    # doesn't match our pattern
    if len(branch_parts) < 3:
        return None     
    if key := re.match(r"^[A-Z]+-[\d]+$", branch_parts[1]):
        return key[0]
    return None        

def prefix_message(msg:str)->str:
    """ creates the updated commit message"""
    if key := get_issue_key():
        return f"#{key}\n{msg}"
    print("\nno smart commit key found, skipping.\n")
    return current

def main() -> int:
    try:
        current = cmd_output("git","log","-1", "--pretty=%B")
        msg = prefix_message(current)
        _ = cmd_output("git","commit","--ammend", msg)
    except CalledProcessError:
        print("\nUnable to parse smart commit key, skipping.\n")
    ## this is a non-blocking hook! 
    return 0


if __name__ == '__main__':
    exit(main())
