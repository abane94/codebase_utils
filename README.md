# codebase_utils

stats.py can be run on a file created from a git log similar to:
git --no-pager log --stat > git_log_v1.txt

if an error pops up about the size of the rename variables, this command can extend it
git config merge.renameLimit 999999
