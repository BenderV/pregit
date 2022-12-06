"""TODO
Delete old DB data
"""

import git
from utils.model import Repository, CommitFile
from utils.repository import RepoWrapper

repositories = Repository.query().filter_by(name="hubtech").all()


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
