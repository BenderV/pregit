from git import Repo
from utils.model import Repository, session
import requests

url = "https://api.github.com/search/repositories?q=stars:%3E100+language:python&per_page=100&page={page}&s=stars&o=desc"

res = requests.get(url.format(page=0))

already_downloaded = [n[0] for n in session.query(Repository.url).all()]

for item in res.json()["items"]:
    if item["git_url"] in already_downloaded:
        continue

    repo_dir = f"./repositories/{item['full_name']}"

    print(f"Clone: {item['name']}")
    Repo.clone_from(item["git_url"], repo_dir)
    session.add(
        Repository(
            name=item["name"],
            url=item["git_url"],
            description=item["description"],
            path=repo_dir,
        )
    )
    session.commit()
