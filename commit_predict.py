from utils.model import CommitFile

changes = CommitFile.query().all()

for change in changes:
    print(change.source_content, change.dest_content)
