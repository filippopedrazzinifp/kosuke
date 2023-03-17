import logging

import gitlab

logger = logging.getLogger(__name__)


class GitlabClient:
    def __init__(self, access_token, project_name, branch_name):
        self.gl = gitlab.Gitlab(
            "https://gitlab.com", private_token=access_token, per_page=200
        )
        self.gl.auth()

        self.project_name = project_name
        self.branch_name = branch_name

    def get_project_commits(self, since):
        project = self.get_project()

        commits = project.commits.list(ref_name=self.branch_name, since=since)
        commits_messages = ""
        for commit in commits:
            commits_messages = commits_messages + commit.title + "\n"
        return commits_messages

    def get_project_files(self):
        project = self.get_project()

        page = 1
        files = []
        while True:
            tree = project.repository_tree(page=page, per_page=100, recursive=True)
            if not tree:
                break
            files.extend(tree)
            page += 1

        python_files = [f for f in files if f['path'].endswith('.py')]
        return python_files

    def get_project(self):
        return self.gl.projects.get(self.project_name)
