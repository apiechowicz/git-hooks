# git-hooks
Repository for simple git hooks written in Python3

# Usage:
In order to use git hooks:
1. Ensure execution rights.
2. Copy desired hook into `.git/hooks` directory in your repository and remove Python script extension.

Example (linux):
```
$ chmod +x prepare-commit-msg.py
$ mv prepare-commit-msg.py <path-to-your-repo>/.git/hooks/prepare-commit-msg
```

Notices:
* in order for hooks to work in non Ubuntu-based system you may need to change [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))
* using hooks from this repository requires Python 3.5+ (due to type hints)
* to configure global git hooks refer to [this](https://stackoverflow.com/questions/2293498/applying-a-git-post-commit-hook-to-all-current-and-future-repos) Stack Overflow thread
