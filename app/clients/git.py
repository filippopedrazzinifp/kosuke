import logging

logger = logging.getLogger(__name__)


class GitClient:
    def __init__(self, client):
        self.client = client

    def get_commits(self, since):
        return self.client.get_commits(since)

    def get_files(self):
        return self.client.get_files()

    def get_project(self):
        return self.client.get_project()
