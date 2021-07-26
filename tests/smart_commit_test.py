import pytest

from pre_commit_hooks.smart_commits import get_issue_key
from pre_commit_hooks.smart_commits import prefix_message
from pre_commit_hooks.smart_commits import main
from pre_commit_hooks.util import cmd_output


def test_no_key(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'feature/no-key-exists')
        assert get_issue_key() is None


def test_has_key(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'feature/TEST-1234/branch')
        assert get_issue_key() == 'TEST-1234'


def test_prefixes_message(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'feature/TEST-1234/branch')
        assert prefix_message("this is a test") == "#TEST-1234\nthis is a test"
