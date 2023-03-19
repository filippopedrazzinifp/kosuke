import logging

from github import Github

from app.clients import git

logger = logging.getLogger(__name__)


class GithubClient(git.GitClient):
    def __init__(self, access_token, repo_name, branch_name):
        self.gh = Github(access_token)
        self.repo_name = repo_name
        self.branch_name = branch_name

    def get_repo_commits(self, since):
        repo = self.get_repo()

        commits = repo.get_commits(since=since, sha=self.branch_name)
        commits_messages = ""
        for commit in commits:
            commits_messages = commits_messages + commit.commit.message + "\n"
        return commits_messages

    def get_repo_files(self):
        repo = self.get_repo()

        tree = repo.get_git_tree(self.branch_name, recursive=True)
        files = tree.tree

        python_files = [f for f in files if f.path.endswith(".py")]
        return python_files

    def get_repo(self):
        return self.gh.get_repo(self.repo_name)
