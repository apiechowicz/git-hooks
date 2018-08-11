#!/usr/bin/env python3
import sys
from re import fullmatch
from subprocess import check_output

SKIP_REBASE_COMMITS = True
SKIP_MERGE_COMMITS = True
BRANCH_NAME_PATTERN = '^(?:feature|bugfix)-(\d+)$'
COMMIT_MESSAGE_TAG_TEMPLATE = '[{}]'
COMMIT_MESSAGE_SEPARATOR = ' '
BRANCH_TAG_PREFIX = '#'  # 'normal' working branches
SPECIAL_BRANCH_TAG = 'HF'  # special branches like master, develop, release branches etc.
MERGE_COMMIT_PATTERN = "^Merge (?:remote-tracking )?branch '[\w-]+' into [\w-]+$"
CAPITALIZE = True
REMOVE_TRAILING_DOT = True


def main() -> None:
    commit_message_file = sys.argv[1]
    branch_name = get_branch_name()
    if SKIP_REBASE_COMMITS and branch_name_indicates_rebase(branch_name):
        return
    commit_message = read_commit_message(commit_message_file)
    if SKIP_MERGE_COMMITS and is_merge_commit(commit_message):
        return
    commit_tag = create_commit_tag(branch_name)
    new_commit_message = update_commit_message_if_needed(commit_message, commit_tag)
    if new_commit_message != commit_message:
        change_commit_message(commit_message_file, new_commit_message)


def get_branch_name() -> str:
    return check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], encoding='utf-8').strip()


def branch_name_indicates_rebase(branch_name: str) -> bool:
    return branch_name == 'HEAD'


def read_commit_message(message_file: str) -> str:
    with open(message_file, 'r') as file:
        return file.read().strip()


def is_merge_commit(commit_message: str) -> bool:
    return fullmatch(MERGE_COMMIT_PATTERN, commit_message) is not None


def create_commit_tag(branch_name: str) -> str:
    match = fullmatch(BRANCH_NAME_PATTERN, branch_name)
    if match:
        return COMMIT_MESSAGE_TAG_TEMPLATE.format(BRANCH_TAG_PREFIX + match.group(1))
    return COMMIT_MESSAGE_TAG_TEMPLATE.format(SPECIAL_BRANCH_TAG)


def update_commit_message_if_needed(commit_message: str, branch_tag: str) -> str:
    if CAPITALIZE:
        commit_message = commit_message.capitalize()
    if REMOVE_TRAILING_DOT:
        commit_message = remove_trailing_dot_if_needed(commit_message)
    if not is_branch_tag_present(commit_message, branch_tag):
        commit_message = add_branch_tag(commit_message, branch_tag)
    return commit_message


def remove_trailing_dot_if_needed(commit_message: str) -> str:
    if commit_message.endswith('.'):
        return commit_message[:-1]
    return commit_message


def is_branch_tag_present(commit_message: str, branch_tag: str) -> bool:
    return commit_message.startswith(branch_tag)


def add_branch_tag(commit_message: str, branch_tag: str) -> str:
    return branch_tag + COMMIT_MESSAGE_SEPARATOR + commit_message


def change_commit_message(commit_message_file_path: str, new_commit_message: str) -> None:
    truncate_file(commit_message_file_path)
    save_message(commit_message_file_path, new_commit_message)


def truncate_file(file_path: str) -> None:
    with open(file_path, 'w') as file_path:
        file_path.truncate()


def save_message(commit_message_file_path: str, new_commit_message: str) -> None:
    with open(commit_message_file_path, 'w') as file:
        file.write(new_commit_message)


if __name__ == '__main__':
    main()
