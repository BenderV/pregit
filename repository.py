import hashlib
import re
import sys

from git import Repo

re_tab = re.compile('[^\t]+')
sys.setrecursionlimit(10000)

class RepoWrapper(Repo):

    def __init__(self, name):
        super(RepoWrapper, self).__init__(name)

    def pprint(commit):
        print(commit)
        print(f"> {commit.message.rstrip()}")
        print('')

    @staticmethod
    def explore(commit, visited=set()):
        if commit.hexsha not in visited:
            visited.add(commit.hexsha)
            yield commit
        for parent in commit.parents:
            yield from RepoWrapper.explore(parent, visited)

    @staticmethod
    def is_commit_merge(commit):
        return len(commit.parents) > 1

    def extract_merge(self, commit):
        """
        Don't find the last merge??
        https://github.com/pallets/flask/pulls?q=is%3Apr+is%3Amerged
        """
        if not is_commit_merge(commit):
            return
        commit_merge = commit
        commit_a, commit_b = commit_merge.parents
        commit_source = self.merge_base(commit_a, commit_b)[0]
        diff_a = self.extract_diff(commit_source.hexsha, commit_a.hexsha)
        diff_b = self.extract_diff(commit_source.hexsha, commit_b.hexsha)
        return {'commit_source':commit_source, 
         'commit_merge':commit_merge, 
         'commit_a':commit_a, 
         'commit_b':commit_b, 
         'diff_a':diff_a, 
         'diff_b':diff_b}

    def read_file(self, commit_sha, path):
        """Altenative ?
        git.Repo().commit(COMMIT_HEX_SHA).tree['subdir/somefile.ext'].data_stream.read()
        """
        try:
            return self.git.show('{}:{}'.format(commit_sha, path))
        except:
            return

    def extract_diff(self, commit1_sha, commit2_sha, file=''):
        return self.git.diff(commit1_sha, commit2_sha, file)

    def find_text_file(self, commit1_sha, commit2_sha):
        output = self.git.diff('--numstat', commit1_sha, commit2_sha)
        files = []
        for line in output.split('\n'):
            if not line:
                continue
            if line.startswith('-'):
                continue
            chunks = re.split('\\t+', line)
            files.append(chunks[(-1)])

        return set(files)

    @staticmethod
    def find_merge_paths_modified(merged):
        paths_a = self.find_text_file(merged['commit_a'].hexsha, merged['commit_source'].hexsha)
        paths_b = self.find_text_file(merged['commit_b'].hexsha, merged['commit_source'].hexsha)
        print(paths_a, paths_b)
        paths_modified = paths_a + paths_b
        return paths_modified

    def extract_file(self, source_sha, dest_sha, path):
        return (
         self.read_file(source_sha, path), self.read_file(dest_sha, path))

    @staticmethod
    def export2file(content):
        hash_object = hashlib.sha256(content.encode())
        name = hash_object.hexdigest()
        with open('./files/' + name, 'w+') as (f):
            f.write(content)
        return name
