"""
Parse repository and extract commit info from merge commit.
commit_file contains:
    - path
    - source_content: content of file in commit_source (save in ./files)
    - dest_content: content of file in commit_dest (save in ./files)
    - diff: diff of file between commit_source and commit_dest
"""

import git

from model import CommitFile, Repository
from repository import RepoWrapper

repositories = Repository.query().all()


def parse_repository(repository):
    repo = repository.git_repo()

    for commit in RepoWrapper.explore(repo.head.commit):
        if len(commit.parents) != 1:
            continue

        commit_source = commit.parents[0]
        commit_dest = commit

        paths = repo.find_text_file(commit_source, commit_dest)
        for path in paths:
            print(commit, path)
            try:
                diff = repo.extract_diff(commit_source.hexsha, commit_dest.hexsha, path)

                source_content, dest_content = repo.extract_file(
                    commit_source.hexsha, commit_dest.hexsha, path
                )

                if source_content:
                    source_content = RepoWrapper.export2file(source_content)

                if dest_content:
                    dest_content = RepoWrapper.export2file(dest_content)

                CommitFile.get_or_create(
                    path=path,
                    source_content=source_content,
                    dest_content=dest_content,
                    diff=diff,
                )
            except git.exc.GitCommandError as e:
                print("Error.")
                print(e)


for repository in repositories:
    print(repository)
    parse_repository(repository)
