import datetime
import logging

from github import Github

from app import settings
from app.clients import git

logger = logging.getLogger(__name__)


class GithubClient(git.GitClient):
    def __init__(self, access_token, repo_name, branch_name):
        self.gh = Github(access_token)
        self.repo_name = repo_name
        self.branch_name = branch_name

    def get_commits(self, since):
        repo = self.get_project()

        commits = repo.get_commits(since=since, sha=self.branch_name)
        commits_messages = ""
        for commit in commits:
            commits_messages = commits_messages + commit.commit.message + "\n"
        return commits_messages

    def get_files(self):
        repo = self.get_project()

        tree = repo.get_git_tree(self.branch_name, recursive=True)
        files = tree.tree

        filtered_files = []
        for file_element in files:
            file = {"path": file_element.path}
            filtered_files.append(file)

        return filtered_files

    def get_file_content(self, file_path):
        repo = self.get_project()
        file = repo.get_contents(file_path, ref=self.branch_name)
        return file.decoded_content.decode()

    def get_project(self):
        return self.gh.get_repo(self.repo_name)

    def get_latest_comment_date(self, pr):
        latest_comment_date = None
        for comment in pr.get_issue_comments():
            comment_date = datetime.datetime.strptime(
                comment.created_at.isoformat(), "%Y-%m-%dT%H:%M:%S.%f"
            )
            if not latest_comment_date or comment_date > latest_comment_date:
                latest_comment_date = comment_date
        return latest_comment_date

    def get_latest_commit_date(self, pr):
        latest_commit_date = None
        for commit in pr.get_commits():
            commit_date = datetime.datetime.strptime(
                commit.commit.author.date.isoformat(), "%Y-%m-%dT%H:%M:%S.%f"
            )
            if not latest_commit_date or commit_date > latest_commit_date:
                latest_commit_date = commit_date
        return latest_commit_date

    def get_pull_requests(self):
        repo = self.get_project()
        return repo.get_pulls(state="open", base=self.branch_name)

    def can_comment(self, pr):
        comments = pr.get_issue_comments()
        if comments.totalCount:
            latest_comment_date = self.get_latest_comment_date(pr)
            latest_commit_date = self.get_latest_commit_date(pr)
            return latest_commit_date > latest_comment_date
        else:
            return True

    def get_pull_request_changes(self, pr):
        return [{"diff": file.patch} for file in pr.get_files()]

    def comment_pull_request(self, pr, message):
        issue = pr.as_issue()
        issue.create_comment(f"# {settings.BOT_NAME} Says \n {message}")
