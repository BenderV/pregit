from git import diff
from model import Repository, Merge, File, Transition, session
from diff import extract_merge_diff
import sys
import uuid
import hashlib
import re

re_tab = re.compile("[^\t]+")

sys.setrecursionlimit(10000)


def explore(commit, visited=set()):
    if commit.hexsha not in visited:
        visited.add(commit.hexsha)
        yield commit
        for parent in commit.parents:
            yield from explore(parent, visited)


# sentry
# pandas
# flask

# master = repo.head.reference
repository = Repository.query().filter_by(path="./repositories/pallets/flask").first()
repo = repository.git_repo()


for ind, commit in enumerate(explore(repo.head.commit)):
    print(ind)
    # Maybe we should store all the commit ?
    for commit_source in commit.parents:
        Transition.get_or_create(
            repo_id=repository.id,
            commit_source_hash=commit_source.hexsha,
            commit_dest_hash=commit.hexsha,
        )

    if len(commit.parents) == 2:
        extract_merge_diff(
            repo, commit.parents[0].hexsha, commit.parents[1].hexsha, commit.hexsha
        )

