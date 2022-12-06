import re

CONFLICT_LINE = 'CONFLICT (content): Merge conflict in '
REGEX_SPLIT = '(<<<<<<< HEAD(.|\n)*?>>>>>>> .{40})'

def extract_merge_diff(repo, commit_hash_a, commit_hash_b, commit_dest):
    repo.git.checkout(commit_hash_a)
    try:
        output = repo.git.merge(commit_hash_b, commit_hash_a)
    except Exception as error:
        try:
            if error.status == 128:
                return
            print('==============================')
            print(commit_hash_a, commit_hash_b)
            output = repo.git.commit('-am "merge"')
            merge_commit_hash = output.split('HEAD ')[1].split(']')[0]
            for line in error.stdout.split('\n'):
                if CONFLICT_LINE in line:
                    path = line.replace(CONFLICT_LINE, '')
                    print(path)
                    file = repo.git.show(f"{merge_commit_hash}:{path}")
                    splits = re.split(REGEX_SPLIT, file)
                    for split in splits:
                        if '<<<<<<<' in split:
                            print(split)

        finally:
            error = None
            del error
