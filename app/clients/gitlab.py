import datetime
import logging

import gitlab

from app import settings
from app.clients import git

logger = logging.getLogger(__name__)


class GitlabClient(git.GitClient):
    def __init__(self, access_token, project_name, branch_name):
        self.gl = gitlab.Gitlab(
            "https://gitlab.com", private_token=access_token, per_page=200
        )
        self.gl.auth()

        self.project_name = project_name
        self.branch_name = branch_name

    def get_commits(self, since):
        project = self.get_project()

        commits = project.commits.list(ref_name=self.branch_name, since=since)
        commits_messages = ""
        for commit in commits:
            commits_messages = commits_messages + commit.title + "\n"
        return commits_messages

    def get_files(self):
        project = self.get_project()

        page = 1
        files = []
        while True:
            tree = project.repository_tree(page=page, per_page=100, recursive=True)
            if not tree:
                break
            files.extend(tree)
            page += 1

        return files

    def get_project(self):
        return self.gl.projects.get(self.project_name)

    def get_file_content(self, file_path):
        project = self.get_project()
        return project.files.get(
            file_path=file_path, ref=project.default_branch
        ).decode()

    def get_latest_comment_date(self, mr):
        latest_comment_date = None
        for comment in mr.notes.list():
            comment_date = datetime.datetime.strptime(
                comment.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if not latest_comment_date or comment_date > latest_comment_date:
                latest_comment_date = comment_date
        return latest_comment_date

    def get_latest_commit_date(self, mr):
        latest_commit_date = None
        for commit in mr.commits():
            commit_date = datetime.datetime.strptime(
                commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if not latest_commit_date or commit_date > latest_commit_date:
                latest_commit_date = commit_date
        return latest_commit_date

    def get_pull_requests(self):
        project = self.get_project()
        return project.mergerequests.list(
            target_branch=self.branch_name, state="opened"
        )

    def can_comment(self, mr):
        comments = mr.notes.list()
        if comments:
            latest_comment_date = self.get_latest_comment_date(mr)
            latest_commit_date = self.get_latest_commit_date(mr)
            return latest_commit_date > latest_comment_date
        else:
            return True

    def get_pull_request_changes(self, mr):
        return mr.changes()["changes"]

    def comment_pull_request(self, mr, message):
        mr.notes.create({"body": f"# {settings.BOT_NAME} Says \n {message}"})
